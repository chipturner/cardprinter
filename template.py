from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import sys

card_width = 2.5 * inch
card_height = 3.5 * inch
cut_gap = inch * 0.2 / 6
border_gap = inch / 16.0

def draw_card(c):
    c.saveState() 
    c.setStrokeColorRGB(0, 1, 0)
    c.roundRect(0, 0, card_width + 2 * cut_gap, card_height + 2 * cut_gap, 0.2 * inch)
    c.restoreState()

    c.saveState() 
    c.setStrokeColorRGB(0, 0, 0)
    c.translate(cut_gap, cut_gap)
    c.roundRect(0, 0, card_width, card_height, 0.2 * inch)
    c.restoreState()

    c.saveState() 
    c.setStrokeColorRGB(1.0, 0, 0)
    c.translate(border_gap + cut_gap, border_gap + cut_gap)
    c.roundRect(0, 0, card_width - 2 * border_gap, card_height - 2 * border_gap, 0.2 * inch)
    c.restoreState()


def create_template(output_file):
    # Page size and margins
    page_width, page_height = letter

    c = canvas.Canvas(str(output_file), pagesize=letter)
    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    for margin_step in range(2):
        margin = 0.1 * (1 + margin_step) * inch
        x0, y0 = margin, margin
        content_width = page_width - 2 * margin
        content_height = page_height - 2 * margin
        c.rect(x0, y0, content_width, content_height)

    margin = 0.2 * inch
    for x_step in range(3):
        for y_step in range(3):
            x = x_step * (10 * cut_gap + card_width) + margin - border_gap
            y = y_step * (2.75 * cut_gap + card_height) + margin - border_gap - cut_gap*.25
            c.saveState()
            c.translate(x, y)
            draw_card(c)
            c.restoreState()
    c.save()

# Example usage
create_template(sys.argv[1])
