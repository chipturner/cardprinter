from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import sys

CARD_WIDTH: float = 2.5 * inch
CARD_HEIGHT: float = 3.5 * inch
CUT_GAP: float = inch * 0.2 / 6
BORDER_GAP: float = inch / 16.0


def draw_card(c: canvas.Canvas) -> None:
    c.saveState()
    c.setStrokeColorRGB(0, 1, 0)
    c.roundRect(0, 0, CARD_WIDTH + 2 * CUT_GAP, CARD_HEIGHT + 2 * CUT_GAP, 0.2 * inch)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(0, 0, 0)
    c.translate(CUT_GAP, CUT_GAP)
    c.roundRect(0, 0, CARD_WIDTH, CARD_HEIGHT, 0.2 * inch)
    c.restoreState()

    c.saveState()
    c.setStrokeColorRGB(1.0, 0, 0)
    c.translate(BORDER_GAP + CUT_GAP, BORDER_GAP + CUT_GAP)
    c.roundRect(
        0, 0, CARD_WIDTH - 2 * BORDER_GAP, CARD_HEIGHT - 2 * BORDER_GAP, 0.2 * inch
    )
    c.restoreState()


def create_template(output_file: str) -> None:
    page_width, page_height = letter

    c: canvas.Canvas = canvas.Canvas(str(output_file), pagesize=letter)
    c.setStrokeColorRGB(0.75, 0.75, 0.75)

    for margin_step in range(2):
        margin: float = 0.1 * (1 + margin_step) * inch
        x0, y0 = margin, margin
        content_width: float = page_width - 2 * margin
        content_height: float = page_height - 2 * margin
        c.rect(x0, y0, content_width, content_height)

    margin: float = 0.2 * inch

    for x_step in range(3):
        for y_step in range(3):
            x: float = x_step * (10 * CUT_GAP + CARD_WIDTH) + margin - BORDER_GAP
            y: float = (
                y_step * (2.75 * CUT_GAP + CARD_HEIGHT)
                + margin
                - BORDER_GAP
                - CUT_GAP * 0.25
            )
            c.saveState()
            c.translate(x, y)
            draw_card(c)
            c.restoreState()

    c.save()


# Example usage
create_template(sys.argv[1])
