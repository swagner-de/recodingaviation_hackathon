from flask import Flask
from model import db
from flask_login import LoginManager


# Create application
app = Flask('Recodingaviation')

# MongoDB settings
app.config.from_pyfile('app.cfg')
lm = LoginManager
db.init_app(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
