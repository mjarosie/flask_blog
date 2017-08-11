from flask import Blueprint
from helpers import object_list
from models import Entry

entries = Blueprint('entries', __name__, template_folder='templates')

@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return object_list('entries/index.html', entries)

@entries.route('/tags/')
def tag_index():
    pass

@entries.route('/tags/<slug>/')
def tag_details(slug):
    pass

@entries.route('/<slug>/')
def detail(slug):
    pass