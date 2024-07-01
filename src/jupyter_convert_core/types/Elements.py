from dataclasses import dataclass
from typing import List


@dataclass
class Element:
    pass


@dataclass
class ContainerElement(Element):
    children: List[Element | str] = None


@dataclass(kw_only=True)
class MdDocument(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdHeading(ContainerElement):
    level: int


@dataclass(kw_only=True)
class MdParagraph(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdLine(Element):
    pass


@dataclass(kw_only=True)
class MdCode(ContainerElement):
    lang: str = None


@dataclass(kw_only=True)
class MdEmphasis(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdStrongEmphasis(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdImage(Element):
    source: str


@dataclass(kw_only=True)
class MdLatex(Element):
    latex: str


@dataclass(kw_only=True)
class MdList(ContainerElement):
    bullet: str
    ordered: bool
    start: int


@dataclass(kw_only=True)
class MdListItem(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdLink(ContainerElement):
    source: str


@dataclass(kw_only=True)
class MdQuote(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdTable(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdTableRow(ContainerElement):
    pass


@dataclass(kw_only=True)
class MdTableCell(ContainerElement):
    header: bool
    align: str
