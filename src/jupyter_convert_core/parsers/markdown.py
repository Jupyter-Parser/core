import builtins
import re
import marko
from marko.helpers import MarkoExtension
from marko import Markdown
from marko.block import Document, Element
from marko.inline import InlineElement
import marko.inline
from ..types import (
    Element as ParsedElement,
    MdDocument,
    MdHeading,
    MdLink,
    MdParagraph,
    MdLine,
    MdCode,
    MdImage,
    MdLatex,
    MdEmphasis,
    MdList,
    MdListItem,
    MdStrongEmphasis,
    MdQuote,
    MdTable,
    MdTableCell,
    MdTableRow,
)
from markdownify import markdownify as md


class Latex(InlineElement):
    pattern = r"\$(.*?)\$"
    parse_children = True

    def __init__(self, match: re.Match):
        self.latex = match.group(0)


class RawMixin:
    def render(self, element: Document):
        return element


RawExtension = MarkoExtension(elements=[Latex], renderer_mixins=[RawMixin])

markdown = Markdown(extensions=[RawExtension, "gfm"])


def get_tree(text: str) -> Document:
    return markdown(text)


def walk(element: Element) -> ParsedElement:
    elem = ParsedElement()

    element_type = type(element)

    match element_type:
        case marko.block.Document:
            elem = MdDocument()
        case marko.block.ThematicBreak:
            return
        case marko.block.List:
            elem = MdList(
                bullet=element.bullet, ordered=element.ordered, start=element.start
            )
        case marko.block.ListItem:
            elem = MdListItem()
        case marko.block.Heading:
            elem = MdHeading(level=element.level)
        case marko.inline.Link | marko.ext.gfm.elements.Url:
            elem = MdLink(source=element.dest)
        case marko.ext.gfm.elements.Paragraph:
            elem = MdParagraph()
        case marko.inline.Emphasis:
            elem = MdEmphasis()
        case marko.inline.StrongEmphasis:
            elem = MdStrongEmphasis()
        case marko.block.BlankLine | marko.inline.LineBreak:
            return MdLine()
        case marko.inline.CodeSpan:
            return MdCode(children=element.children)
        case marko.block.CodeBlock | marko.block.FencedCode:
            elem = MdCode(lang=element.lang)
        case marko.inline.Literal | marko.inline.RawText | marko.inline.Literal:
            return element.children
        case builtins.str:
            return element
        case marko.inline.Image:
            return MdImage(source=element.dest)
        case marko.block.Quote:
            elem = MdQuote()
        case marko.ext.gfm.elements.Table:
            elem = MdTable()
        case marko.ext.gfm.elements.TableRow:
            elem = MdTableRow()
        case marko.ext.gfm.elements.TableCell:
            elem = MdTableCell(align=element.align, header=element.header)
        case marko.block.HTMLBlock:
            tree = get_tree(md(element.body))
            return walk(tree)

    if element_type == Latex:
        return MdLatex(latex=element.latex)

    elem.children = list(map(walk, element.children))

    return elem


def parse_markdown(markdown: str) -> MdDocument:
    tree = get_tree(markdown)
    return walk(tree)
