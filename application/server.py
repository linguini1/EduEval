# Runs the Flask server which hosts the web application
__author__ = "Hamnah Qureshi"

# Imports
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import pandas as pd

# Constants
from werkzeug.datastructures import FileStorage

STATIC_FOLDER: str = ".\\webapp\\build\\static"
TEMPLATE_FOLDER: str = ".\\webapp\\build"
API_ROUTE: str = "/api"
API_PORT: int = 8000
REACT_HOST: str = "localhost:3000"

# Flask application
app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
cors = CORS(app)
app.config["SERVER_NAME"] = f"localhost:{API_PORT}"
app.config["CORS_HEADERS"] = "Content-Type"


# Webpage route
@app.route("/", methods=["GET"])
def index():
    """The homepage of the website where HTML will be served. React Router handles URLS beyond this."""
    return render_template("index.html")


# API Routes
@app.route('/upload', methods=["POST"])
@cross_origin(origins=REACT_HOST)
def upload():
    """API route for uploading CSV file with professorial ratings for one school."""

    file = request.files.get("file")
    if file is None:
        return 400  # Bad request (no file given)

    # file.save('data/userdata.csv') #if we want to save the csv file
    df = pd.read_csv(file)
    df.to_parquet('data/data_file.parquet.gzip')

    return 200  # Success


if __name__ == '__main__':
    app.run(debug=True, port=API_PORT)
