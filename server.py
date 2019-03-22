from flask import Flask, render_template, request, jsonify, session, redirect, g
import requests
import os
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from cassandra.cluster import Cluster
import uuid
from cassandra.query import dict_factory



auth = HTTPBasicAuth()

# cluster = Cluster(['cassandra'])
cluster = Cluster(['127.0.0.1'])


session = cluster.connect()

session.row_factory = dict_factory


app = Flask(__name__, template_folder="templates")
# app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']


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

    id =""
    username = ""

    password_hash = ""

    name = ""

    email = ""

    # 1 for admin, 2 for normal user
    role = 2

    def __init__(self, username, name, email):
        self.username = username
        self.name = name
        self.email = email

    def update_id(self, id):
        self.id = id

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def update_name(self, name):
        self.name = name

    def update_email(self, email):
        self.email = email

    def update_role(self,role):
        self.role = role

    def update_password_hash(self, password_hash):
        self.password_hash = password_hash

    def update_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        print("that fucking thing" + data['id'])
        prepared_statement = session.prepare('SELECT ID ,Username,Role FROM CCMiniProject.users WHERE ID= ?')
        rows = session.execute(prepared_statement, (uuid.UUID(data['id']),))
        if not rows:
            return None
        else:
            user = User(rows[0][u'username'], "", "")
            user.update_role(rows[0][u'role'])
            return user


@app.route('/api/users/createuser', methods=['POST'])
def create_user():
    if request is None:
        return jsonify({'error': 'missing arguments!'}), 400
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    name = request.json.get('name')
    if username is None or password is None:
        # missing arguments
        return jsonify({'error': 'missing arguments!'}), 400
    prepared_statement = session.prepare("SELECT * FROM CCMiniProject.users WHERE Username = ?;")
    rows = session.execute(prepared_statement,(username,))
    if rows:
        if rows[0][u'username'] == username:
            # existing user
            return jsonify({'error': 'existing user!'}), 400
    user = User(username=username, name=name, email=email)
    user.hash_password(password)
    rows = session.execute("INSERT INTO CCMiniProject.users (ID,Username,Password_hash, Name, Email, Role) VALUES (%s,%s,%s,%s,%s,%s);", (uuid.uuid4(),user.username, user.password_hash, user.name, user.email, 2))
    return jsonify({'username': user.username, 'name': user.name, 'email': user.email}), 201


@app.route('/api/users/updateuser/<username>', methods=['PUT'])
@auth.login_required
def update_user(username):
    if request is None:
        return jsonify({'error': 'missing arguments!'}), 400
    password = request.json.get('password')
    email = request.json.get('email')
    name = request.json.get('name')
    if password is None or email is None or name is None:
        # missing arguments
        return jsonify({'error': 'missing arguments!'}), 400
    prepared_statement = session.prepare('SELECT ID, Username FROM CCMiniProject.users WHERE Username = ?')
    rows = session.execute(prepared_statement, (username,))
    # if not admin then not allowed to update or create other users
    if g.user.role == 2:
        if (rows is None) or (not rows):
            return jsonify({'error': 'only authorized to update your user'}), 401
        else:
            if rows[0][u'username'] != g.user.username:
                # existing user
                return jsonify({'error': 'only authorized to update your user'}), 401
            user = User(username=username, name=name, email=email)
            user.hash_password(password)
            user.update_id(rows[0][u'id'])
            prepared_statement = session.prepare("UPDATE CCMiniProject.users SET Password_hash = ?, Name = ?, Email = ? WHERE ID = ?")
            rows = session.execute(prepared_statement, (user.password_hash, user.name, user.email, user.id))
            return jsonify({'username': user.username, 'name': user.name, 'email': user.email}), 200
    # if admin then allowed to update and create users
    else:
        # if user doesn't exist create new one
        if (rows is None) or (not rows):
            user = User(username=username, name=name, email=email)
            user.hash_password(password)
            rows = session.execute("INSERT INTO CCMiniProject.users (ID,Username,Password_hash, Name, Email, Role) VALUES (%s,%s,%s,%s,%s,%s)", (uuid.uuid4(),user.username, user.password_hash, user.name, user.email,2))
            return jsonify({'username': user.username, 'name': user.name, 'email': user.email}), 201
        # if user exists then update
        else:
            user = User(username=username, name=name, email=email)
            user.hash_password(password)
            user_id = rows[0][u'id']
            prepared_statement = session.prepare("UPDATE CCMiniProject.users SET Password_hash = ?, Name = ?, Email = ? WHERE ID = ?")
            rows = session.execute(prepared_statement, (user.password_hash, user.name, user.email, user_id))
            return jsonify({'username': user.username, 'name': user.name, 'email': user.email}), 200

@app.route('/api/users/deleteuser/<username>', methods=['DELETE'])
@auth.login_required
def delete_user(username):
    prepared_statement = session.prepare('SELECT ID,Username FROM CCMiniProject.users WHERE Username = ?')
    rows = session.execute(prepared_statement, (username,))
    # if not admin not allowed to delete other users
    if g.user.role == 2:
        # if user to be deleted doesn't exist, show unauthorized instead of user doesn't exist. Non admins shouldn't
        # know which users exist and which do not.
        if (rows is None) or (not rows):
            return jsonify({'error': 'unauthorized delete request!'}), 401
        else:
            if rows[0][u'username'] != g.user.username:
                # existing user
                return jsonify({'error': 'unauthorized delete request!'}), 401
            id_to_delete = rows[0][u'id']
            prepared_statement = session.prepare("DELETE FROM CCMiniProject.users WHERE ID = ?")
            rows = session.execute(prepared_statement, (id_to_delete,))
            return jsonify({'data': 'user deleted'}), 200
    # if admin allowed to delete any user
    else:
        # if user does't exist
        if (rows is None) or (not rows):
            return jsonify({'error': 'user not found'}), 404
        user_id = rows[0][u'id']
        prepared_statement = session.prepare("DELETE FROM CCMiniProject.users WHERE ID = ?")
        rows = session.execute(prepared_statement, (user_id,))
        return jsonify({'data': 'user deleted'}), 200


@app.route('/api/token', methods=["GET"])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/get_crimes',  methods=['GET'])
@auth.login_required
def get_crimes():
    if request is None:
        return jsonify({'error': 'missing arguments!'}), 400
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
    if request is None:
        return jsonify({'error': 'missing arguments!'}), 400
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
    if request is None:
        return jsonify({'error': 'missing arguments!'}), 400
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
    if request is None:
        return jsonify({'error': 'missing arguments!'}), 400
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
        prepared_statement = session.prepare("SELECT ID,Username,Password_hash,Role FROM CCMiniProject.users WHERE Username = ?;")
        rows = session.execute(prepared_statement, (username_or_token,))
        if not rows:
            return False
        else:
            user = User(rows[0][u'username'],"","")
            user.update_password_hash(rows[0][u'password_hash'])
            user.update_role(rows[0][u'role'])
            user.update_id(str(rows[0][u'id']))
        if not user.verify_password(password):
            return False
    g.user = user
    return True


# If we're running in stand alone mode, run the application
if __name__ == '__main__':

    app.secret_key = secret_key
    context = ('cert.pem', 'key.pem')
    app.run(debug=False/True, ssl_context=context)