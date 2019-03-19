from flask import Flask, render_template, request, jsonify, session, redirect
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
from pprint import pprint
import os
from OpenSSL import SSL




app = Flask(__name__, template_folder="templates")

crime_url_template = 'https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={data}'
categories_url_template = 'https://data.police.uk/api/crime-categories?date={date}'


secret_key = os.urandom(12)


@app.route('/crimestat',  methods=['GET'])
def crimechart():
    my_latitude = request.args.get('lat','51.52369')
    my_longitude = request.args.get('lng','-0.0395857')
    my_date = request.args.get('date','2018-11')
    crime_url = crime_url_template.format(lat = my_latitude,
                                          lng = my_longitude,
                                          data = my_date)
    resp = requests.get(crime_url)
    if resp.ok:
        crimes = resp.json()
    else:
        print(resp.reason)
    pprint(crimes)
    return render_template('home.html')


# Create a URL route in our application for "/"
@app.route('/')
def login():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('login.html')


@app.route('/home', methods=["POST"])
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    username = request.form.get('username')
    password = request.form.get('password')
    if password != "1234":
        return redirect("/", code=302)
    else:
        session['username'] = username
        return render_template('home.html')


@app.route('/records/', methods=['GET'])
def get_records():
    return jsonify(all_records)


@app.route('/records/<bandname>', methods=['GET','DELETE'])
def get_albums_by_band(bandname):
    albums = [band['albums'] for band in all_records if band['name'] == bandname]
    if len(albums)==0:
        return jsonify({'error':'band name not found!'}), 404
    else:
        response = [album['title'] for album in albums[0]]
        return jsonify(response), 200


@app.route('/records/<bandname>/<albumtitle>', methods=['GET'])
def get_songs_by_band_and_album(bandname, albumtitle):
    albums = [band['albums'] for band in all_records if band['name'] == bandname]
    if len(albums)==0:
        return jsonify({'error':'band name not found!'}), 404
    else:
        songs = [album['songs'] for album in albums[0] if album['title'] == albumtitle]
        if len(songs)==0:
            return jsonify({'error':'album title not found!'}), 404
        else:
            return jsonify(songs[0]), 200


# If we're running in stand alone mode, run the application
if __name__ == '__main__':

    app.secret_key = secret_key
    context = ('cert.pem', 'key.pem')
    app.run(debug=False/True, ssl_context=context)