from starlette_wtf import StarletteForm
import wtforms
from wtforms.validators import DataRequired, Optional


class NoteForm(StarletteForm):
    id = wtforms.IntegerField(validators=[Optional()])
    text = wtforms.StringField(validators=[DataRequired()])
    completed = wtforms.BooleanField()
    delete = wtforms.BooleanField()
