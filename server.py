from flask import Flask, render_template, request, jsonify, session, redirect, g
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
from pprint import pprint
import os
from OpenSSL import SSL
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from cassandra.cluster import Cluster
from flask.ext.cqlalchemy import CQLAlchemy
import uuid

auth = HTTPBasicAuth()

app = Flask(__name__, template_folder="templates")


# app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
# app.config['CASSANDRA_KEYSPACE'] = "cqlengine"
# db = CQLAlchemy(app)


secret_key = os.urandom(12)



app.config['SECRET_KEY'] = secret_key

API_KEY = 'AIzaSyDmLyS-tAL6evGdKrTjKA-DcgSD6lMuiAI'


crime_url_template = 'https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={data}'
outcome_url_template = 'https://data.police.uk/api/outcomes-for-crime/{id}'
categories_url_template = 'https://data.police.uk/api/crime-categories?date={date}'

place_url_template = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={place}&key={key}'


user_hash = "$6$rounds=656000$kyl9UY6kcV3sAT4u$G9Tu3XycW2HpSDe4tFJK/i28t5haDGb0FsBxCgg5VjArO2SgP6GVEOi450N1FKYyXnrEbUNqK.EFiCPbsabSi0"

# class User(db.Model):
class User:

    # id = db.columns.UUID(primary_key=True, default=uuid.uuid4)
    # username = db.columns.Text(required=True)
    #
    # password_hash = db.columns.Text(required=True)
    #
    # name = db.columns.Text(required=False)
    #
    # email = db.columns.Text(required=False)

    id = ""
    username = ""

    password_hash = ""

    name = ""

    email = ""

    def __init__(self, username, name, email):
        self.username = username
        self.name = name
        self.email = email

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def update_name(self, name):
        self.name = name

    def update_email(self, email):
        self.email = email

    def update_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': 1})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User("sakis", "", "")
        user.hash_password("1234")
        return user


@app.route('/api/createuser', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    name = request.json.get('name')
    if username is None or password is None:
        # missing arguments
        return jsonify({'error': 'missing arguments!'}), 400
    # if User.query.filter_by(username = username).first() is not None:
    #     # existing user
    #     return jsonify({'error': 'existing user!'}), 400
    user = User(username=username, name=name, email=email)
    user.hash_password(password)
    # db.session.add(user)
    # db.session.commit()
    return jsonify({'username': user.username, 'name': user.name, 'email': user.email}), 201


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/get_crimes',  methods=['GET'])
@auth.login_required
def get_crimes():
    my_latitude = request.args.get('lat')
    my_longitude = request.args.get('lng')
    my_date = request.args.get('date')
    if (my_latitude is None) or (my_longitude is None) or (my_date is None):
        return jsonify({'error': 'missing arguments'}), 400
    crime_url = crime_url_template.format(lat = my_latitude,
                                          lng = my_longitude,
                                          data = my_date)
    resp = requests.get(crime_url)
    if resp.ok:
        crimes = resp.json()
    else:
        return jsonify({'error': resp.reason}), resp.status_code
    return jsonify({'data': crimes}), 200


@app.route('/api/get_crimes_at_place',  methods=['GET'])
@auth.login_required
def get_crimes_at_place():
    place = request.args.get('place')
    if place is None:
        return jsonify({'error': 'missing arguments'}), 400
    print(place)
    place_url = place_url_template.format(place = place,
                                          key = API_KEY)
    resp = requests.get(place_url)
    if resp.ok:
        places = resp.json()
        name = places['results'][0]['name']
        location = places['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        crime_url = crime_url_template.format(lat =lat,
                                              lng = lng,
                                              data = None)
        resp = requests.get(crime_url)
        if resp.ok:
            crimes = resp.json()
        else:
            return jsonify({'error': resp.reason}), resp.status_code
        name_dict = {'name': name}
        location_dict = {'location': location}
        crimes_dict = {'crimes': crimes}
        data_to_return1 = dict(name_dict, **location_dict)
        data_to_return2 = dict(data_to_return1, **crimes_dict)
        return jsonify({'data': data_to_return2}), 200

    else:
        print("error")
        return jsonify({'error': resp.reason}), resp.status_code


@app.route('/api/get_crime_outcome',  methods=['GET'])
@auth.login_required
def get_crime_outcome():
    id = request.args.get('id')
    if id is None:
        return jsonify({'error': 'missing arguments'}), 400
    outcome_url = outcome_url_template.format(id=id)
    resp = requests.get(outcome_url)
    if resp.ok:
        outcome = resp.json()
    else:
        return jsonify({'error': resp.reason}), resp.status_code
    return jsonify({'data': outcome}), 200


@app.route('/api/get_crime_categories',  methods=['GET'])
@auth.login_required
def get_crime_categories():
    date = request.args.get('date')
    if date is None:
        return jsonify({'error': 'missing arguments'}), 400
    categories_url = categories_url_template.format(date=date)
    resp = requests.get(categories_url)
    if resp.ok:
        categories = resp.json()
    else:
        return jsonify({'error': resp.reason}), resp.status_code
    return jsonify({'data': categories}), 200



# Create a URL route in our application for "/"
@app.route('/')
def home():
    return jsonify({'data': 'Welcome to the Cloud Computing Mini Project REST API. To start using the API please create a user'})


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User("username1", "", "")
        user.hash_password("1234")
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# If we're running in stand alone mode, run the application
if __name__ == '__main__':

    app.secret_key = secret_key
    context = ('cert.pem', 'key.pem')
    app.run(debug=False/True, ssl_context=context)