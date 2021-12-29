from breathe.directives import BaseDirective
from breathe.file_state_cache import MTimeError
from breathe.project import ProjectError
from breathe.renderer.filter import Filter
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.target import create_target_handler

from docutils.nodes import Node

from docutils.parsers.rst.directives import unchanged_required, flag

from typing import Any, List


class _DoxygenBaseItemDirective(BaseDirective):
    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
    }
    has_content = False

    def create_finder_filter(self, namespace: str, name: str) -> Filter:
        """Creates a filter to find the node corresponding to this item."""

        return self.filter_factory.create_member_finder_filter(namespace, name, self.kind)

    def run(self) -> List[Node]:
        try:
            namespace, name = self.arguments[0].rsplit("::", 1)
        except ValueError:
            namespace, name = "", self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimeError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        finder_filter = self.create_finder_filter(namespace, name)

        # TODO: find a more specific type for the Doxygen nodes
        matches: List[Any] = []
        finder.filter_(finder_filter, matches)

        if len(matches) == 0:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = self.create_warning(project_info, kind=self.kind, display_name=display_name)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{display_name}" {tail}')

        target_handler = create_target_handler(self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_outline_filter(self.options)

        node_stack = matches[0]
        mask_factory = NullMaskFactory()
        return self.render(
            node_stack, project_info, filter_, target_handler, mask_factory, self.directive_args
        )


class DoxygenVariableDirective(_DoxygenBaseItemDirective):
    kind = "variable"


class DoxygenDefineDirective(_DoxygenBaseItemDirective):
    kind = "define"


class DoxygenConceptDirective(_DoxygenBaseItemDirective):
    kind = "concept"

    def create_finder_filter(self, namespace: str, name: str) -> Filter:
        # Unions are stored in the xml file with their fully namespaced name
        # We're using C++ namespaces here, it might be best to make this file
        # type dependent
        #
        xml_name = "%s::%s" % (namespace, name) if namespace else name
        return self.filter_factory.create_compound_finder_filter(xml_name, "concept")


class DoxygenEnumDirective(_DoxygenBaseItemDirective):
    kind = "enum"


class DoxygenEnumValueDirective(_DoxygenBaseItemDirective):
    kind = "enumvalue"

    def create_finder_filter(self, namespace: str, name: str) -> Filter:
        return self.filter_factory.create_enumvalue_finder_filter(name)


class DoxygenTypedefDirective(_DoxygenBaseItemDirective):
    kind = "typedef"


class DoxygenUnionDirective(_DoxygenBaseItemDirective):
    kind = "union"

    def create_finder_filter(self, namespace: str, name: str) -> Filter:
        # Unions are stored in the xml file with their fully namespaced name
        # We're using C++ namespaces here, it might be best to make this file
        # type dependent
        #
        xml_name = "%s::%s" % (namespace, name) if namespace else name
        return self.filter_factory.create_compound_finder_filter(xml_name, "union")
