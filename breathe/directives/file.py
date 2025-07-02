from __future__ import annotations

import os.path
from typing import TYPE_CHECKING

from docutils.parsers.rst.directives import flag, unchanged_required

from breathe import parser, path_handler, project, renderer
from breathe.cpp_util import split_name
from breathe.directives import BaseDirective
from breathe.renderer import filter
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.sphinxrenderer import SphinxRenderer
from breathe.renderer.target import create_target_handler

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from typing import Any, ClassVar

    from docutils.nodes import Node


def path_matches(location: str, target_file: str) -> bool:
    if path_handler.includes_directory(target_file):
        # If the target_file contains directory separators then
        # match against the same length at the end of the location
        #
        location_match = location[-len(target_file) :]
        return location_match == target_file

    # If there are no separators, match against the whole filename
    # at the end of the location
    #
    # This is to prevent "Util.cpp" matching "PathUtil.cpp"
    #
    location_basename = os.path.basename(location)
    return location_basename == target_file


def location_matches(location: parser.Node_locationType | None, target_file: str) -> bool:
    return location is not None and path_matches(location.file, target_file)


def namespace_matches(name: str, node: parser.Node_compounddefType):
    to_find = "::".join(split_name(name)[:-1])
    return any(to_find == "".join(ns) for ns in node.innernamespace) or any(
        to_find == "".join(ns) for ns in node.innerclass
    )


def create_file_filter(
    filename: str,
    options: Mapping[str, Any],
    *,
    init_valid_names: Iterable[str] | None = None,
) -> filter.DoxFilter:
    valid_names: set[str] = set()
    if init_valid_names:
        valid_names.update(init_valid_names)

    outline_filter = filter.create_outline_filter(options)

    def filter_(nstack: filter.NodeStack) -> bool:
        if not outline_filter(nstack):
            return False

        node = nstack.node
        parent = nstack.parent
        if isinstance(node, parser.Node_compounddefType):
            if node.kind == parser.DoxCompoundKind.file:
                # Gather the "namespaces" attribute from the
                # compounddef for the file we're rendering and
                # store the information in the "valid_names" list
                if location_matches(node.location, filename):
                    valid_names.update("".join(ns) for ns in node.innernamespace)
                    valid_names.update("".join(ns) for ns in node.innerclass)

            if node.kind != parser.DoxCompoundKind.namespace:
                # Ignore compounddefs which are from another file
                # (normally means classes and structs which are in a
                # namespace that we have other interests in) but only
                # check it if the compounddef is not a namespace
                # itself, as for some reason compounddefs for
                # namespaces are registered with just a single file
                # location even if they namespace is spread over
                # multiple files
                return location_matches(node.location, filename)

        elif isinstance(node, parser.Node_refType):
            name = "".join(node)
            if isinstance(parent, parser.Node_compounddefType) and nstack.tag in {
                "innerclass",
                "innernamespace",
            }:
                # Take the valid_names and every time we handle an
                # innerclass or innernamespace, check that its name
                # was one of those initial valid names so that we
                # never end up rendering a namespace or class that
                # wasn't in the initial file. Notably this is
                # required as the location attribute for the
                # namespace in the xml is unreliable.
                if name not in valid_names:
                    return False

                # Ignore innerclasses and innernamespaces that are inside a
                # namespace that is going to be rendered as they will be
                # rendered with that namespace and we don't want them twice
                if namespace_matches(name, parent):
                    return False

        elif isinstance(node, parser.Node_memberdefType):
            # Ignore memberdefs from files which are different to
            # the one we're rendering. This happens when we have to
            # cross into a namespace xml file which has entries
            # from multiple files in it
            return path_matches(node.location.file, filename)

        return True

    return filter_


def file_finder_filter(
    filename: str,
    d_parser: parser.DoxygenParser,
    project_info: project.ProjectInfo,
    index: parser.DoxygenIndex,
    matches: list[filter.FinderMatch],
) -> None:
    for c in index.file_compounds:
        if not path_matches(c.name, filename):
            continue
        for cd in d_parser.parse_compound(c.refid, project_info).root.compounddef:
            if cd.kind != parser.DoxCompoundKind.file:
                continue
            matches.append([renderer.TaggedNode(None, cd)])


class _BaseFileDirective(BaseDirective):
    """Base class handle the main work when given the appropriate file and project info to work
    from.
    """

    directive_name: ClassVar[str]

    # We use inheritance here rather than a separate object and composition, because so much
    # information is present in the Directive class from the docutils framework that we'd have to
    # pass way too much stuff to a helper object to be reasonable.

    def handle_contents(self, file_: str, project_info: project.ProjectInfo) -> list[Node]:
        d_index = self.get_doxygen_index(project_info)
        matches: list[filter.FinderMatch] = []
        file_finder_filter(file_, self.dox_parser, project_info, d_index, matches)

        if len(matches) > 1:
            warning = self.create_warning(None, file=file_, directivename=self.directive_name)
            return warning.warn('{directivename}: Found multiple matches for file "{file} {tail}')
        elif not matches:
            warning = self.create_warning(None, file=file_, directivename=self.directive_name)
            return warning.warn('{directivename}: Cannot find file "{file} {tail}')

        target_handler = create_target_handler(self.options, self.env)
        filter_ = create_file_filter(file_, self.options)

        node_list: list[Node] = []
        for node_stack in matches:
            object_renderer = SphinxRenderer(
                self.dox_parser.app,
                project_info,
                [tv.value for tv in node_stack],
                self.state,
                self.state.document,
                target_handler,
                self.dox_parser,
                filter_,
            )

            mask_factory = NullMaskFactory()
            context = renderer.RenderContext(node_stack, mask_factory, self.directive_args)
            value = node_stack[0].value
            assert isinstance(value, parser.Node)
            node_list.extend(object_renderer.render(value, context))

        return node_list


class DoxygenFileDirective(_BaseFileDirective):
    directive_name = "doxygenfile"

    required_arguments = 0
    optional_arguments = 3
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        "allow-dot-graphs": flag,
        "sections": unchanged_required,
    }
    has_content = False

    def run(self):
        """Get the file from the argument and the project info from the factory."""

        file_ = self.arguments[0]
        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except project.ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("doxygenfile: %s" % e)

        return self.handle_contents(file_, project_info)


class AutoDoxygenFileDirective(_BaseFileDirective):
    directive_name = "autodoxygenfile"

    required_arguments = 1
    option_spec = {
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        "allow-dot-graphs": flag,
        "sections": unchanged_required,
    }
    has_content = False

    def run(self):
        """Get the file from the argument and extract the associated project info for the named
        project given that it is an auto-project.
        """

        file_ = self.arguments[0]
        try:
            project_info = self.project_info_factory.retrieve_project_info_for_auto(self.options)
        except project.ProjectError as e:
            warning = self.create_warning(None)
            return warning.warn("autodoxygenfile: %s" % e)

        return self.handle_contents(file_, project_info)
