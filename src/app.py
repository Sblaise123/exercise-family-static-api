"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Perso

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

@app.route('/member', methods=['POST'])
def add_family_member():
    age = request.json.get("age")
    first_name = request.json.get("first_name")
    lucky_numbers = request.json.get("lucky_numbers")
    jackson_family.add_member({

        "id": jackson_family._generateId,
        "first_name": first_name,
        "last_name": jackson_family.last_name,
        "age": age,
        "lucky_numbers": lucky_numbers,

    })
    return jsonify(response_body), 200


@app.route("/delete/<int:id>", methods=['DELETE'])
def delete_family_member(id):
    jackson_family.delete_member(id)
    response={"Family Member Deleted": True}
    return jsonify(response), 200

@app.route("/member/<int:id>", methods=['GET'])
def get_individual_fmaily_member(id):
    member = jackson_family.get_member(id)
    response_body = member
    return jsonify(response), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
