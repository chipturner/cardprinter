from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import csv
import sys
from pathlib import Path
import random


def create_pdf_with_word_wrap(input_file, output_file):
    # Page size and margins
    page_width, page_height = letter
    margin = 0.5 * inch
    content_width = page_width - 2 * margin
    content_height = page_height - 2 * margin

    # Rectangle dimensions
    rect_width = 2.5 * inch
    rect_height = 3.5 * inch

    # Spacing between rectangles
    x_spacing = inch / 16.0
    y_spacing = inch / 16.0

    # Create a PDF canvas
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
    lines = []
    with open(input_file, "r") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        for row in reader:
            lines.append(row)

    lines.pop(0)
    random.shuffle(lines)
    for i, line in enumerate(lines):
        # Add a new page if the current one is full
        if i % 9 == 0 and i != 0:
            c.showPage()

        # Calculate position
        x = margin + (i % 3) * (rect_width + x_spacing)
        y = (
            page_height
            - margin
            - rect_height
            - ((i // 3) % 3) * (rect_height + y_spacing)
            + 0.15 * inch
        )

        # Draw inner rectangle with rounded corners
        inner_rect_x = x + 0.1 * inch
        inner_rect_y = y + 0.1 * inch
        inner_rect_width = rect_width
        inner_rect_height = rect_height

        # Create a paragraph for the text
        p = Paragraph(f"<b>{line[0].strip()}</b>", style)

        # Calculate text width and height for word wrap
        text_width = inner_rect_width - 0.5 * inch
        text_height = inner_rect_height - 0.1 * inch

        # Draw the paragraph in the rectangle
        p.wrapOn(c, text_width, text_height)
        p.drawOn(
            c,
            inner_rect_x + 0.25 * inch,
            inner_rect_y + (inner_rect_height - p.height) / 1.5,
        )
        c.setLineWidth(2)
        if len(line) == 1:
            c.setStrokeColorRGB(0, 0, 255)
        else:
            c.setStrokeColorRGB(255, 0, 0)
        c.roundRect(
            inner_rect_x + 0.1 * inch,
            inner_rect_y + 0.1 * inch,
            inner_rect_width - 0.2 * inch,
            inner_rect_height - 0.2 * inch,
            0.2 * inch,
            stroke=1,
        )
        # c.roundRect(inner_rect_x, inner_rect_y, inner_rect_width, inner_rect_height, 0.2 * inch)
        # c.rect(x, y, rect_width, rect_height)

        if len(line) == 2:
            p = Paragraph(f"<i> - {line[1].strip()}</i>", attribution_style)
            p.wrapOn(c, text_width, text_height)
            p.drawOn(
                c,
                inner_rect_x + 0.25 * inch,
                inner_rect_y + (inner_rect_height - p.height) * 0.1,
            )

    c.save()


# Example usage
input_file = Path(sys.argv[1])
output_file = input_file.with_suffix(".pdf")
create_pdf_with_word_wrap(input_file, output_file)
