from docutils import nodes
import textwrap


def format_parser_error(name, error, filename, state, lineno, do_unicode_warning):
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
            *unicode_explanation
        ),
        state.document.reporter.warning(
            warning + explanation + unicode_explanation_text, line=lineno
        ),
    ]


class RenderContext:
    def __init__(
        self, node_stack, mask_factory, directive_args, domain: str = "", child: bool = False
    ) -> None:
        self.node_stack = node_stack
        self.mask_factory = mask_factory
        self.directive_args = directive_args
        self.domain = domain
        self.child = child

    def create_child_context(self, data_object) -> "RenderContext":
        node_stack = self.node_stack[:]
        node_stack.insert(0, self.mask_factory.mask(data_object))
        return RenderContext(node_stack, self.mask_factory, self.directive_args, self.domain, True)
