from pathlib import Path
from flask import Flask, request, send_file
import tempfile

import print_cards

from typing import Optional, TypeVar


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        input_file = tempfile.NamedTemporaryFile(delete=False)
        input_filename = input_file.name
        input_file.write(request.files["file"].read())
        input_file.close()

        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        output_filename = output_file.name
        output_file.close()

        assert request.files["file"].filename is not None
        visible_name = request.files["file"].filename.replace(".csv", ".pdf")

        print_cards.create_template(Path(input_filename), Path(output_filename))
        return send_file(
            output_filename,
            as_attachment=True,
            download_name=visible_name,
        )

    return """
    <!doctype html>
    <title>Upload a File</title>
    <h1>Upload a File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9193, debug=False)
