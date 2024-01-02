# Card Drawing Project

This is a collection of scripts for generating printable PDFs of cards for simple customizable card games as well as printing a PDF of a framing jig for then laser cutting the printed cards.

## Usage

Run `python print_cards.py PATH_TO_CSV` to execute the program.

## Scripts

- `print_cards.py`: This is the main script of the project. It defines the card dimensions and the `draw_card` function which draws a card using the ReportLab library.  The CSV file contains one or two columns of the card text and optional attribution.

- `jig_template.py`: This creates the actual jig PDF which can then be cut on a typical laser cutter such as a Glowforge.
