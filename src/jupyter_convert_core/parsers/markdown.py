import re
from marko.helpers import MarkoExtension
from marko import Markdown
from marko.block import Document
from marko.inline import InlineElement


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
