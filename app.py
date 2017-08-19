from flask import Flask, g
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import Configuration  # import configuration data.
from flask_login import LoginManager, current_user


app = Flask(__name__)
app.config.from_object(Configuration)  # use values from our Configuration object.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.before_request
def _before_request():
    g.user = current_user

bcrypt = Bcrypt(app)

