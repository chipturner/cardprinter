import csv
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

CARD_WIDTH: float = 2.5 * inch
CARD_HEIGHT: float = 3.5 * inch
CUT_GAP: float = inch * 0.2 / 6
BORDER_GAP: float = inch / 16.0
PARA_LEADING_SIZE = 18


@dataclass
class Quote:
    """
    Represents a quote with its contents, attribution, and date string.
    """

    contents: str
    attribution: Optional[str]
    date_string: str


def draw_card(
    c: canvas.Canvas, line: Quote, style: Paragraph, attribution_style: Paragraph
) -> None:
    c.saveState()
    c.setStrokeColorRGB(0, 1, 0)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(0, 0, 0)
    c.translate(CUT_GAP, CUT_GAP)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(1.0, 0, 0)
    c.translate(BORDER_GAP + CUT_GAP, BORDER_GAP + CUT_GAP)
    c.setLineWidth(2)
    if not line.attribution:
        c.setStrokeColorRGB(0, 0, 1)
    else:
        c.setStrokeColorRGB(1, 0, 0)

    c.roundRect(
        0, 0, CARD_WIDTH - 2 * BORDER_GAP, CARD_HEIGHT - 2 * BORDER_GAP, 0.2 * inch
    )

    p = Paragraph(f"<b>{line.contents.strip()}</b>", style)

    # Calculate text width and height for word wrap
    text_width = 2.0 * inch - BORDER_GAP - CUT_GAP
    text_height = 2.0 * inch - BORDER_GAP
    corners = 0.25 * inch, text_height - 0.50 * inch, text_width, text_height

    # Draw the paragraph in the rectangle
    p.wrapOn(c, text_width, text_height)
    p.drawOn(c, corners[0], text_height - p.height / 2 + 0.25 * inch)
    # c.roundRect(*corners, 0)

    if line.attribution:
        p = Paragraph(f"<i> - {line.attribution.strip()}</i>", attribution_style)
        p.wrapOn(c, text_width, text_height)
        p.drawOn(
            c,
            corners[0],
            0.15 * inch,
        )

    c.restoreState()


def create_template(input_file: Path, output_file: Path) -> None:
    # Page size and margins
    page_width, page_height = letter

    c = canvas.Canvas(str(output_file), pagesize=letter)

    # Styles for paragraphs
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.alignment = 1  # Center alignment
    style.textColor = colors.black
    style.fontSize = 14
    style.leading = PARA_LEADING_SIZE

    attribution_style = styles["Normal"].clone("Attribiution")
    attribution_style.alignment = 2  # Right alignment
    attribution_style.textColor = colors.black
    attribution_style.fontSize = 10
    attribution_style.leading = PARA_LEADING_SIZE

    # Read lines from the input file
    lines: List[Quote] = []
    with open(input_file, "r") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        for row in reader:
            contents = row[0]
            attribution = row[1] if len(row) > 2 else None
            date_string = row[-1]
            lines.append(Quote(contents, attribution, date_string))

    lines.pop(0)
    random.shuffle(lines)

    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    for margin_step in range(2):
        margin = 0.1 * (1 + margin_step) * inch
        x0, y0 = margin, margin
        content_width = page_width - 2 * margin
        content_height = page_height - 2 * margin

    margin = 0.2 * inch
    i = 0
    for line in lines:
        # Skip line if the last column is not empty
        if line.date_string:
            continue

        # Add a new page if the current one is full
        if i % 9 == 0 and i != 0:
            c.showPage()
        x_step = (i // 3) % 3
        y_step = i % 3
        x = x_step * (10 * CUT_GAP + CARD_WIDTH) + margin - BORDER_GAP
        y = (
            y_step * (2.75 * CUT_GAP + CARD_HEIGHT)
            + margin
            - BORDER_GAP
            - CUT_GAP * 0.25
        )
        c.saveState()
        c.translate(x, y)
        draw_card(c, line, style, attribution_style)
        c.restoreState()
        i += 1
    c.save()


def main():
    input_directory: Path = Path(sys.argv[1])

    for csv_file in input_directory.glob("*.csv"):
        output_file: Path = csv_file.with_suffix(".pdf")
        create_template(csv_file, output_file)

if __name__ == "__main__":
    main()