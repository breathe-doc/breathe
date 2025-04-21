<<<<<<< HEAD
from __future__ import annotations

||||||| 542ae9b
from docutils import nodes
=======
from __future__ import annotations

from docutils import nodes
>>>>>>> memberdef-in-groups
import textwrap
from typing import Generic, NamedTuple, TYPE_CHECKING, TypeVar, Union

if TYPE_CHECKING:
    from breathe import parser
    from breathe.renderer import mask
    from breathe.directives.index import RootDataObject

    DataObject = Union[parser.NodeOrValue, RootDataObject]
    T_data_object = TypeVar("T_data_object", bound=DataObject, covariant=True)
else:
    T_data_object = TypeVar("T_data_object", covariant=True)

from docutils import nodes


def format_parser_error(
    name: str, error: str, filename: str, state, lineno: int, do_unicode_warning: bool = False
) -> list[nodes.Node]:
    warning = '%s: Unable to parse xml file "%s". ' % (name, filename)
    explanation = "Reported error: %s. " % error

    unicode_explanation_text = ""
    unicode_explanation = []
    if do_unicode_warning:
        unicode_explanation_text = (
            textwrap.dedent(
                """
        Parsing errors are often due to unicode errors associated with the encoding of the original
        source files. Doxygen propagates invalid characters from the input source files to the
        output xml."""
            )
            .strip()
            .replace("\n", " ")
        )
        unicode_explanation = [nodes.paragraph("", "", nodes.Text(unicode_explanation_text))]

    return [
        nodes.warning(
            "",
            nodes.paragraph("", "", nodes.Text(warning)),
            nodes.paragraph("", "", nodes.Text(explanation)),
            *unicode_explanation,
        ),
        state.document.reporter.warning(
            warning + explanation + unicode_explanation_text, line=lineno
        ),
    ]


if TYPE_CHECKING:

    class TaggedNode(NamedTuple, Generic[T_data_object]):
        tag: str | None
        value: T_data_object

else:
    # Python 3.9 and 3.10 don't allow multiple-inheritance with NamedTuple
    class TaggedNode(NamedTuple):
        tag: str | None
        value: ...


class RenderContext:
    def __init__(
        self,
        node_stack: list[TaggedNode],
        mask_factory: mask.MaskFactoryBase,
        directive_args,
        domain: str = "",
        child: bool = False,
    ) -> None:
        self.node_stack = node_stack
        self.mask_factory = mask_factory
        self.directive_args = directive_args
        self.domain = domain
        self.child = child

<<<<<<< HEAD
    def create_child_context(self, data_object) -> RenderContext:
||||||| 542ae9b
    def create_child_context(self, data_object) -> "RenderContext":
=======
    def create_child_context(
        self, data_object: parser.NodeOrValue, tag: str | None = None
    ) -> RenderContext:
>>>>>>> memberdef-in-groups
        node_stack = self.node_stack[:]
        node_stack.insert(0, TaggedNode(tag, self.mask_factory.mask(data_object)))
        return RenderContext(node_stack, self.mask_factory, self.directive_args, self.domain, True)
