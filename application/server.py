# Runs the Flask server which hosts the web application
__author__ = "Hamnah Qureshi"

# Imports
from processing import create_professor_index, analyze_sentiment, create_feedback_listing
from flask import Flask, request, render_template, Response
from flask_cors import CORS, cross_origin
import pandas as pd
import threading

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
SURVEY_DATA: pd.DataFrame | None = None
FEEDBACK: pd.DataFrame | None = None


# Processing function
def evaluate_feedback() -> None:
    """Creates the listing of positive and negative feedback for every professor and their courses."""
    global SURVEY_DATA
    global FEEDBACK

    if SURVEY_DATA is None:
        print("No data to evaluate feedback.")
        return

    analyzed_data = analyze_sentiment(SURVEY_DATA)  # Associate with sentiments
    analyzed_data = analyzed_data.groupby(["professor", "course"], group_keys=True)  # Group data
    combos = list(analyzed_data.groups.keys())
    analyzed_data = analyzed_data.apply(lambda x: x)  # Make searchable
    FEEDBACK = create_feedback_listing(analyzed_data, combos)
    print(FEEDBACK)


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

    # Create feedback listing in another thread
    threading.Thread(target=evaluate_feedback).start()

    return Response(status=200)  # Success


@app.route("/index", methods=["GET"])
@cross_origin()
def prof_index():
    return PROF_INDEX


@app.route("/feedback/<prof>/<course>", methods=["GET"])
@cross_origin(origins="*")
def feedback(prof: str, course: str):
    """Returns the feedback associated with this professor and course combination."""

    courses = FEEDBACK.get(prof, dict()) if FEEDBACK is not None else dict()
    summaries = courses.get(course)

    if summaries is None:
        return {"positive": "No ratings.", "negative": "No ratings."}

    return {"positive": summaries.get("positive"), "negative": summaries.get("negative")}


if __name__ == '__main__':
    app.run(debug=True, port=API_PORT)
