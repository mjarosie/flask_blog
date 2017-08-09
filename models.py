import datetime, re
from app import db


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()


entry_tags = db.Table('entry_tags',
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                      db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
                      )


class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    tags = db.relationship('Tag', secondary=entry_tags, backref=db.backref('entries', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)  # Call parent constructor.
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry: {}>'.format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)

    def __init(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag {}>'.format(self.name)
