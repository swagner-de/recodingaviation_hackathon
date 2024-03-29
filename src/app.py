#!/usr/bin/env python3

from flask import Flask, request, jsonify
from model import db, User
from flask_httpauth import HTTPBasicAuth

# Create application
app = Flask('Recodingaviation')

# MongoDB settings
app.config.from_pyfile('app.cfg')

auth = HTTPBasicAuth()

@auth.verify_password
def verify_pw(username, password):
    return User.check_pw(username, password)

db.init_app(app)

@app.route('/create_trip', methods=['GET'])
@auth.login_required
def create_trip_from_pnr():
    pnr = request.args.get('pnr')
    if not pnr:
        # Bad Request
        return 400
    u = User.objects.get(email=auth.username())
    from map_booking_code import get_trip
    t = get_trip(pnr, u)
    if not t:
        # Not found
        return 404
    t.save()
    # Created
    return jsonify(t), 201

@app.route('/current_legs', methods=['GET'])
@auth.login_required
def get_current_legs():
    u = User.objects.get(email=auth.username())
    from trip_handler import get_current_connect_info
    return jsonify(get_current_connect_info(user=u))

@app.route('/bags', methods=['GET'])
@auth.login_required
def get_bag_journey():
    u = User.objects.get(email=auth.username())
    from trip_handler import get_bags_info
    return jsonify(get_bags_info(user=u))

@app.route('/sorrounding', methods=['GET'])
def get_sorrounding_pois():
    gate = request.args.get('gate')
    departure = request.args.get('departure') == 'true'
    from api.ams_wayfinding import get_geometry
    geo = get_geometry(gate, departure)
    if not geo:
        return 'Gate not found', 400
    from analysis.ams_pois import calculate_closest
    return jsonify(calculate_closest(
        geo['x'],
        geo['y'],
        geo['z']
    ))

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
