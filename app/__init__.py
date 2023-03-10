from flask import Flask
from config import Config
from .models import db
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)



from . import routes
from . import models
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)