from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from API.pipeline.pipeline import scrap_meta_data, business_number_from_name

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# * ---------- Create App --------- *
app = Flask(__name__)
CORS(app, support_credentials=True)

# * ---------- DATABASE CONFIG --------- *
client = MongoClient("mongodb://user:user@54.37.157.250:27017/admin")
DB = client['kpmg']
DB_TABLE = DB.company


@app.route('/data-from-business-number/<string:business_number>', methods=['GET'])
@cross_origin(supports_creditentials=True)
def data_from_business_number(business_number):
    company_data_from_db = DB_TABLE.find_one({'business_number': business_number})
    
    if company_data_from_db:
        del company_data_from_db['_id']
        meta_data = company_data_from_db
    else:
        meta_data = scrap_meta_data(business_number)
        meta_data_to_insert_db = meta_data.copy()
        DB_TABLE.insert_one(meta_data_to_insert_db)
    return jsonify(meta_data)


@app.route('/get-number-from-name/<string:companyName>', methods=['GET'])
@cross_origin(supports_creditentials=True)
def get_number_from_name(companyName):
    names_and_numbers = business_number_from_name(companyName)
    return jsonify(names_and_numbers)


# * ---------- Run Server ---------- *
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=os.environ['PORT']) -> DOCKER
