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
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
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
    return "ALL GREAT", 200
@app.route('/user', methods=['GET'])
def handle_hello():

    all_people = User.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    
    return jsonify(all_people), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
