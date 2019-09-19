from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import os
from werkzeug.utils import secure_filename
from API.pipeline.utils import scrap_meta_data, business_number_from_name

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# * ---------- Create App --------- *
app = Flask(__name__)
CORS(app, support_credentials=True)

# * ---------- DATABASE CONFIG --------- *
#DATABASE_URL = os.environ['DATABASE_URL']
#engine = create_engine(DATABASE_URL)


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


@app.route('/data-from-business-number/<int:business_number>', methods=['GET'])
def data_from_business_number(business_number):
    meta_data = scrap_meta_data(business_number)
    print(meta_data)
    return jsonify(meta_data)


@app.route('/get-number-from-name/<string:companyName>', methods=['GET'])
def get_number_from_name(companyName):
    names_and_numbers = business_number_from_name(companyName)
    print(names_and_numbers)
    return jsonify(names_and_numbers)


# * ---------- Run Server ---------- *
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=os.environ['PORT']) -> DOCKER
