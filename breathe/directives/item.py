from __future__ import annotations

from breathe.directives import BaseDirective
from breathe.file_state_cache import MTimeError
from breathe.project import ProjectError
from breathe.renderer.mask import NullMaskFactory
from breathe.renderer.target import create_target_handler

from docutils.nodes import Node

from docutils.parsers.rst.directives import unchanged_required, flag

from typing import cast, ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import NotRequired, TypedDict
    else:
        from typing_extensions import NotRequired, TypedDict

    from breathe.renderer import TaggedNode
    from breathe.renderer.filter import DoxFilter

    DoxBaseItemOptions = TypedDict(
        "DoxBaseItemOptions",
        {"path": str, "project": str, "outline": NotRequired[None], "no-link": NotRequired[None]},
    )
else:
    DoxBaseItemOptions = None


class _DoxygenBaseItemDirective(BaseDirective):
    kind: ClassVar[str]

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
    }
    has_content = False

    def create_finder_filter(self, namespace: str, name: str) -> DoxFilter:
        """Creates a filter to find the node corresponding to this item."""

        return self.filter_factory.create_member_finder_filter(namespace, name, self.kind)

    def run(self) -> list[Node]:
        options = cast(DoxBaseItemOptions, self.options)

        namespace, _, name = self.arguments[0].rpartition("::")

        try:
            project_info = self.project_info_factory.create_project_info(options)
        except ProjectError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        try:
            finder = self.finder_factory.create_finder(project_info)
        except MTimeError as e:
            warning = self.create_warning(None, kind=self.kind)
            return warning.warn("doxygen{kind}: %s" % e)

        finder_filter = self.create_finder_filter(namespace, name)

        matches: list[list[TaggedNode]] = []
        finder.filter_(finder_filter, matches)

        if len(matches) == 0:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = self.create_warning(project_info, kind=self.kind, display_name=display_name)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{display_name}" {tail}')

        target_handler = create_target_handler(options, project_info, self.state.document)
        filter_ = self.filter_factory.create_outline_filter(options)

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

    def create_finder_filter(self, namespace: str, name: str) -> DoxFilter:
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

    def create_finder_filter(self, namespace: str, name: str) -> DoxFilter:
        return self.filter_factory.create_enumvalue_finder_filter(name)


class DoxygenTypedefDirective(_DoxygenBaseItemDirective):
    kind = "typedef"


class DoxygenUnionDirective(_DoxygenBaseItemDirective):
    kind = "union"

    def create_finder_filter(self, namespace: str, name: str) -> DoxFilter:
        # Unions are stored in the xml file with their fully namespaced name
        # We're using C++ namespaces here, it might be best to make this file
        # type dependent
        #
        xml_name = "%s::%s" % (namespace, name) if namespace else name
        return self.filter_factory.create_compound_finder_filter(xml_name, "union")
