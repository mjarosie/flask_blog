import wtforms
from wtforms.validators import DataRequired

from models import Entry


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

    def save_entry(self, entry):
        """Populates the given entry with the form data and re-generates the entry's slug based on the new title."""
        self.populate_obj(entry)
        entry.generate_slug()
        return entry
