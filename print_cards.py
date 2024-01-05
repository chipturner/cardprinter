import csv
from pathlib import Path
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import sys
from typing import List

CARD_WIDTH: float = 2.5 * inch
CARD_HEIGHT: float = 3.5 * inch
CUT_GAP: float = inch * 0.2 / 6
BORDER_GAP: float = inch / 16.0


def draw_card(
    c: canvas.Canvas, line: List[str], style: Paragraph, attribution_style: Paragraph
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
    if len(line) == 1:
        c.setStrokeColorRGB(0, 0, 1)
    else:
        c.setStrokeColorRGB(1, 0, 0)
    c.roundRect(
        0, 0, CARD_WIDTH - 2 * BORDER_GAP, CARD_HEIGHT - 2 * BORDER_GAP, 0.2 * inch
    )

    p = Paragraph(f"<b>{line[0].strip()}</b>", style)

    # Calculate text width and height for word wrap
    text_width = 2.0 * inch
    text_height = 2.0 * inch

    # Draw the paragraph in the rectangle
    p.wrapOn(c, text_width, text_height)
    p.drawOn(
        c,
        0.25 * inch,
        text_height - 0.25 * inch,
    )

    if len(line) == 2:
        p = Paragraph(f"<i> - {line[1].strip()}</i>", attribution_style)
        p.wrapOn(c, text_width, text_height)
        p.drawOn(
            c,
            0.25 * inch,
            (p.height) * 1.5,
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

    attribution_style = styles["Normal"].clone("Attribiution")
    attribution_style.alignment = 2  # Right alignment
    attribution_style.textColor = colors.black
    attribution_style.fontSize = 10

    # Read lines from the input file
    lines: List[List[str]] = []
    with open(input_file, "r") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        for row in reader:
            lines.append(row)

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
        if line[-1].strip():
            continue
        i += 1
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
    c.save()

input_directory: Path = Path(sys.argv[1])

for csv_file in input_directory.glob("*.csv"):
    output_file: Path = csv_file.with_suffix(".pdf")
    create_template(csv_file, output_file)
