from flask import Blueprint, render_template, request
from helpers import object_list
from models import Entry, Tag

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
    """List all blog entries ordered by date of creation."""
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
    """List all tags."""
    tags = Tag.query.order_by(Tag.name)
    return object_list('entries/tag_index.html', tags)


@entries.route('/tags/<slug>/')
def tag_detail(slug):
    """Show list of blog entries with the given tag."""
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/tag_detail.html', entries, tag=tag)


@entries.route('/<slug>/')
def detail(slug):
    """Show the given entry."""
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)


def entry_list(template, query, **context):
    """Filter a given query by 'q' parameter and insert it into given template."""
    search = request.args.get('q')
    if search:
        query = query.filter((Entry.body.contains(search)) | (Entry.title.contains(search)))
    return object_list(template, query, **context)
