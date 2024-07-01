from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class CellType(Enum):
    code = "code"
    markdown = "markdown"


class OutputType(Enum):
    stream = "stream"
    display_data = "display_data"


@dataclass
class Output:
    output_type: OutputType
    text: Optional[str] = None
    image: Optional[bytes] = None


@dataclass
class Cell:
    cell_type: CellType
    source: str
    outputs: List[Output]
