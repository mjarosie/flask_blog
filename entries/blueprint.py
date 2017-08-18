import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from helpers import object_list
from models import Entry, Tag, entry_tags
from entries.forms import EntryForm, ImageForm
from app import app, db
from werkzeug.utils import secure_filename
from flask_login import login_required

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
    """List all blog entries ordered by date of creation."""
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
    """List all tags."""
    tags = Tag.query.join(entry_tags).distinct().order_by(Tag.name)
    return object_list('entries/tag_index.html', tags)


@entries.route('/tags/<slug>/')
def tag_detail(slug):
    """Show list of blog entries with the given tag."""
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/tag_detail.html', entries, tag=tag)


@entries.route('/image-upload/', methods=['GET', 'POST'])
@login_required
def image_upload():
    if request.method == 'POST':
        form = ImageForm(request.form)
        if form.validate():
            image_file = request.files['file']
            filename = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
            if filename.split('.')[-1] not in ('png', 'jpg', 'tiff', 'gif'):
                flash('Error: "{}" does not have a supported format.'.format(os.path.basename(filename)), 'danger')
                return redirect(url_for('entries.index'))
            image_file.save(filename)
            flash('Saved "{}"'.format(os.path.basename(filename)), 'success')
            return redirect(url_for('entries.index'))
    else:  # If GET request received.
        form = ImageForm()
    return render_template('entries/image_upload.html', form=form)


@entries.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            from app import db
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            flash('Entry "{}" created successfully.'.format(entry.title), 'success')
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:  # If GET request received.
        form = EntryForm()
    return render_template('entries/create.html', form=form)


@entries.route('/<slug>/')
def detail(slug):
    """Show the given entry."""
    entry = get_entry_or_404(slug)
    return render_template('entries/detail.html', entry=entry)


@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    """Show the form for editing an entry (GET) or save the edited entry(POST)."""
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        # Fill a form model with data from page form.
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            # Save data from form model to database entry.
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            flash('Entry "{}" has been saved.'.format(entry.title), 'success')
            # Redirect to the edited entry detail view.
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm(obj=entry)
    return render_template('entries/edit.html', entry=entry, form=form)


@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
@login_required
def delete(slug):
    """Show the form for deleting an entry (GET) or delete the entry(POST)."""
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        entry.status = Entry.STATUS_DELETED
        db.session.add(entry)
        db.session.commit()
        flash('Entry "{}" has been deleted.'.format(entry.title), 'success')
        return redirect(url_for('entries.index'))

    return render_template('entries/delete.html', entry=entry)


def entry_list(template, query, **context):
    """Filter a given query by 'q' parameter and insert it into given template."""
    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    query = query.filter(Entry.status.in_(valid_statuses))
    search = request.args.get('q')
    if search:
        query = query.filter(
            Entry.status == (Entry.body.contains(search)) | (Entry.title.contains(search)))

    return object_list(template, query, **context)


def get_entry_or_404(slug):
    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    return Entry.query.filter((Entry.slug == slug) & (Entry.status.in_(valid_statuses))).first_or_404()
