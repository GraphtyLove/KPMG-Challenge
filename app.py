from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import os
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# * ---------- Create App --------- *
app = Flask(__name__)
CORS(app, support_credentials=True)

# * ---------- DATABASE CONFIG --------- *
DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)

# * ---------- Default page --------- *
@app.route('/', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def index():
    return render_template('index.html')


# * ---------- Upload a file on the server ---------- *
@app.route('/upload', methods=['POST'])
@cross_origin(supports_creditentials=True)
def upload():
    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(FILE_PATH + '/assets/uploaded_files/' + filename)
    return "File uploaded at: ", FILE_PATH + '/assets/uploaded_files/' + filename

# * ---------- Classify a document ---------- *
@app.route('/classify', methods=['POST'])
@cross_origin(supports_creditentials=True)
def classify():
    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(FILE_PATH + '/assets/uploaded_files/' + filename)
    print("File uploaded at: ", FILE_PATH + '/assets/uploaded_files/' + filename)
    # !!! TO DO !!! (put document over the pipeline)
    return 'Document well classified.'


# * ---------- Run Server ---------- *
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=os.environ['PORT']) -> DOCKER
