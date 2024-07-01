from typing import List
from ..types import Cell, CellType, OutputType, Output
import base64
from .markdown import parse_markdown


def parse_jupyter(data: dict):
    cells: List[Cell] = []

    for cell in data["cells"]:
        if not cell["source"]:
            continue

        cell_type: CellType = None
        source = "".join(cell["source"])

        match cell["cell_type"]:
            case "markdown":
                cell_type = CellType.markdown
                source = parse_markdown(source)
            case "code":
                cell_type = CellType.code

        outputs: List[OutputType] = []

        if "outputs" in cell:
            for output in cell["outputs"]:
                output_type: OutputType = None
                text: str = None
                image: bytes = None

                match output["output_type"]:
                    case "stream":
                        output_type = OutputType.stream
                        text = "".join(output["text"])
                    case "display_data":
                        output_type = OutputType.display_data

                        data = output["data"]

                        if "text/plain" in data:
                            text = "".join(data["text/plain"])

                        if "image/png" in data:
                            image = base64.b64decode(data["image/png"])

                outputs.append(Output(output_type=output_type, text=text, image=image))

        cells.append(Cell(cell_type=cell_type, source=source, outputs=outputs))

    return cells
