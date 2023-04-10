# Runs the Flask server which hosts the web application
__author__ = "Hamnah Qureshi"

# Imports
from processing import create_professor_index
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import pandas as pd
from io import StringIO
import json

# Constants
STATIC_FOLDER: str = ".\\webapp\\build\\static"
TEMPLATE_FOLDER: str = ".\\webapp\\build"
API_ROUTE: str = "/api"
API_PORT: int = 5000
REACT_HOST: str = "localhost:3000"

# External paths
SURVEY_DATA_PATH: str = "data/data_file.parquet.gzip"
INDEX_FILE: str = "data/index.json"

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
@app.route("/upload", methods=["POST"])
@cross_origin(origins=REACT_HOST)
def upload():
    """API route for uploading CSV file with professorial ratings for one school."""

    file = request.files.get("file")
    if file is None:
        return 400  # Bad request (no file given)

    # file.save('data/userdata.csv') #if we want to save the csv file

    df = pd.read_csv(file)  # type:ignore
    prof_index = create_professor_index(df)

    print(df)
    df.to_parquet(SURVEY_DATA_PATH)  # Save dataframe
    with open(INDEX_FILE, 'w') as file:  # Save prof index for dropdowns
        json.dump(prof_index, file)

    return 200  # Success


if __name__ == '__main__':
    app.run(debug=True, port=API_PORT)
