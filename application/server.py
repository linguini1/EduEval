# Imports
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)  # Creates a Flask applicaton
cors = CORS(app)  # Enable CORS
app.config['CORS_HEADERS'] = 'Content-Type'  # Allow the 'Content-Type' header in CORS requests


# API route for uploading the file
@app.route('/upload', methods=['POST'])
@cross_origin(origin='localhost:3000')
def upload():
    file = request.files['file']
    # file.save('data/userdata.csv') #if we want to save the csv file
    df = pd.read_csv(file)
    df.to_parquet('data/data_file.parquet.gzip')
    return 'File uploaded successfully'


if __name__ == '__main__':
    # Run API on port 5000
    app.run(debug=True, port=5000)
