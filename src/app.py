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
        return 400
    u = User.objects.get(email=auth.username())
    from map_booking_code import get_trip
    t = get_trip(pnr, u)
    t.save()
    return jsonify(t), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)