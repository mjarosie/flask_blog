import wtforms
from wtforms.validators import DataRequired

from models import Entry, Tag


class TagField(wtforms.StringField):
    def _value(self):
        if self.data:
            # Display tags as a comma-separated list.
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')

        # Filter out empty tags.
        tag_names = [name.strip() for name in raw_tags if name.strip()]

        # Query for any tags that are already saved.
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

        # Derive tags with new names.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tag(name=name)
                    for name
                    in new_names
                    ]

        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []


class EntryForm(wtforms.Form):
    """Form used to create new blog entries. Both title and body are required."""
    title = wtforms.StringField('Title', validators=[DataRequired()])
    body = wtforms.TextAreaField('Body', validators=[DataRequired()])
    status = wtforms.SelectField(
        'Entry status',
        choices=(
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')
        ),
        coerce=int
    )
    tags = TagField('Tags', description='Separate multiple tags with commas.')
    slug = wtforms.StringField('User-friendly URL', render_kw={'readonly': True})

    def save_entry(self, entry):
        """Populates the given entry with the form data and re-generates the entry's slug based on the new title."""
        self.populate_obj(entry)
        entry.generate_slug()
        return entry

class ImageForm(wtforms.Form):
    file = wtforms.FileField('Image file')