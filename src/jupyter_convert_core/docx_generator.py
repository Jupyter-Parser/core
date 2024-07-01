from typing import List
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shape import InlineShape
from .types import Cell, CellType
from io import BytesIO


def scale_picture(picture: InlineShape, new_width):
    aspect_ratio = float(picture.height) / float(picture.width)
    picture.width = new_width
    picture.height = int(aspect_ratio * new_width)


def generate_document(cells: List[Cell]) -> bytes:
    document = Document()

    section = document.sections[0]

    max_picture_width = section.page_width - \
        (section.left_margin + section.right_margin)

    styles = document.styles

    code_style = styles.add_style("code", WD_STYLE_TYPE.PARAGRAPH)
    code_output_style = styles.add_style(
        "code_output", WD_STYLE_TYPE.PARAGRAPH)

    for cell in cells:
        if cell.cell_type == CellType.code:
            code = document.add_paragraph()
            code.style = code_style
            code.add_run(cell.source)

            for output in cell.outputs:
                code_output = document.add_paragraph()
                code_output.style = code_output_style
                run = code_output.add_run()

                if output.text:
                    run.add_text(output.text)
                if output.image:
                    picture = run.add_picture(BytesIO(output.image))
                    if picture.width > max_picture_width:
                        scale_picture(picture, max_picture_width)

    file = BytesIO()

    document.save(file)

    file.seek(0)

    return file.read()
