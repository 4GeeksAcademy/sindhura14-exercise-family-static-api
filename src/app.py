"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

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

#get all members
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200

#add a new member
@app.route('/members',methods=['POST'])
def handle_add_member():
     request_body = request.json
     firstName = request_body['first_name']
     members = jackson_family.get_all_members()
     exists = list(filter(lambda member : member['first_name'] == firstName,members ))
     if(len(exists) > 0):
        raise APIException('member already exists',status_code = 400)
     else :
       jackson_family.add_member(request_body)
       res = jackson_family.get_all_members()
       return jsonify(res),200


#get a specific member
@app.route('/members/<int:member_id>',methods=['GET'])
def handle_get_member(member_id):
    result = jackson_family.get_member(member_id)
    if(len(result)>0):
        return jsonify(result[0])
    else:
        raise APIException('Invalid request',status_code = 400)
        
#delete a member
@app.route('/members/<int:member_id>',methods=['DELETE'])
def handle_delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if(len(result) >0):
        return jsonify(result),200
    else:
        raise APIException('Invalid request',status_code = 400)




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
