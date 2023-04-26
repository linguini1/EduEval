# Runs the Flask server which hosts the web application
__author__ = "Hamnah Qureshi"

# Imports
from processing import create_professor_index
from flask import Flask, request, render_template, Response
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
cors = CORS(app, origins=REACT_HOST)
app.config["SERVER_NAME"] = f"localhost:{API_PORT}"
app.config["CORS_HEADERS"] = "Content-Type"

# Global variables
PROF_INDEX: dict[str, list[str]] = dict()
SURVEY_DATA: pd.DataFrame = None


# Webpage route
@app.route("/", methods=["GET"])
def index():
    """The homepage of the website where HTML will be served. React Router handles URLS beyond this."""
    return render_template("index.html")


# API Routes
@app.route("/upload", methods=["POST"])
@cross_origin()
def upload():
    """API route for uploading CSV file with professorial ratings for one school."""

    file = request.files.get("file")
    if file is None:
        return Response(status=400)  # Bad request (no file given)

    # Read csv as dataframe and create an index of professors to courses
    global SURVEY_DATA
    global PROF_INDEX
    SURVEY_DATA = pd.read_csv(file)  # type:ignore
    PROF_INDEX = create_professor_index(SURVEY_DATA)

    return Response(status=200)  # Success


@app.route("/courses", methods=["GET"])
@cross_origin()
def courses():
    """API route for getting a list of all courses."""

    # Empty index
    if not PROF_INDEX:
        return []

    all_courses: list[str] = []
    for prof, course_list in PROF_INDEX.items():
        all_courses.extend(course_list)
    return all_courses


@app.route("/courses/<prof>", methods=["GET"])
@cross_origin()
def courses_by_prof(prof: str):
    """API route for getting a list of all courses."""
    return PROF_INDEX.get(prof, list())  # Returns empty list if prof is not found


@app.route("/profs", methods=["GET"])
@cross_origin()
def profs():
    """API route for getting a list of all professors."""
    return list(PROF_INDEX.keys())


if __name__ == '__main__':
    app.run(debug=True, port=API_PORT)
