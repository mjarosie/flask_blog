from flask import Blueprint, redirect, render_template, request, url_for
from helpers import object_list
from models import Entry, Tag
from entries.forms import EntryForm
from app import db

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
    """List all blog entries ordered by date of creation."""
    entries = Entry.query.filter(Entry.status == Entry.STATUS_PUBLIC).order_by(Entry.created_timestamp.desc())
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


@entries.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            from app import db
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:  # If GET request received.
        form = EntryForm()
    return render_template('entries/create.html', form=form)


@entries.route('/<slug>/')
def detail(slug):
    """Show the given entry."""
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    # print(entry.tags.order_by(Tag.name.desc()).all())
    # entry.tags = entry.tags.order_by(Tag.name.desc()).all()
    return render_template('entries/detail.html', entry=entry)


@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    """Show the form for editing an entry (GET) or save the edited entry(POST)."""
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    if request.method == 'POST':
        # Fill a form model with data from page form.
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            # Save data from form model to database entry.
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            # Redirect to the edited entry detail view.
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm(obj=entry)
    return render_template('entries/edit.html', entry=entry, form=form)


def entry_list(template, query, **context):
    """Filter a given query by 'q' parameter and insert it into given template."""
    search = request.args.get('q')
    if search:
        query = query.filter(
            Entry.status == (Entry.body.contains(search)) | (Entry.title.contains(search)))
    return object_list(template, query, **context)
