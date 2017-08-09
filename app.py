from flask import Flask
from config import Configuration # import our configuration data.
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Configuration)  # use values from our Configuration object.
db = SQLAlchemy(app)
