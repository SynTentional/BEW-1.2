from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from grocery_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

##Authentication

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)


from grocery_app.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()