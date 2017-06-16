from flask import Flask
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

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
