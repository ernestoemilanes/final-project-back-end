"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, UserIntake
#from models import Person

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    # Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    usercheck = User.query.filter_by(email=email).first()
    if usercheck == None:
        return jsonify({"msg": "Bad email or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
@app.route('/create-account', methods=['POST'])
def handle_user():

    # First we get the payload json
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'first_name' not in body:
        raise APIException('You need to specify the first_name', status_code=400)
    if 'last_name' not in body:
        raise APIException('You need to specify the last_name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)

 
    # at this point, all data has been validated, we can proceed to inster into the bd
    user1 = User(first_name=body['first_name'], email=body['email'], last_name=body['last_name'], password=body['password'])
    db.session.add(user1)
    db.session.commit()
    access_token = create_access_token(identity=body['email'])
    return jsonify(access_token=access_token), 200
@app.route('/user', methods=['GET'])
# @jwt_required
def handle_hello():

    all_people = User.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    
    return jsonify(all_people), 200

@app.route('/create-intake', methods=['POST'])
def handle_user_intake():

    # First we get the payload json
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    # if 'email' not in body:
    #     raise APIException('You need to specify the email', status_code=400)
    # if 'first_name' not in body:
    #     raise APIException('You need to specify the first_name', status_code=400)
    # if 'last_name' not in body:
    #     raise APIException('You need to specify the last_name', status_code=400)
    # if 'password' not in body:
    #     raise APIException('You need to specify the password', status_code=400)

 
    # at this point, all data has been validated, we can proceed to inster into the bd
    user_intake = UserIntake(user_id=body['user_id'], item_name=body['item_name'], nf_calories=body['nf_calories'], nf_calories_from_fat=body['nf_calories_from_fat'], nf_protein=body['nf_protein'], nf_saturated_fats=body['nf_saturated_fats'], nf_sugars=body['nf_sugars'], nf_sodium=body['nf_sodium'], nf_dietary_fiber=body['nf_dietary_fiber'])
    db.session.add(user_intake)
    db.session.commit()
    access_token = create_access_token(identity=body['user_id'])
    return jsonify(access_token=access_token), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
