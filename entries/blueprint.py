from flask import Blueprint, render_template
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
def tag_detail(slug):
    pass


@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)
