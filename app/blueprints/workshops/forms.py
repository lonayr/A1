from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length

class WorkshopForm(FlaskForm):
    title = StringField('عنوان الورشة', validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(min=10)])
    date = DateTimeLocalField('التاريخ والوقت', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('المكان', validators=[Length(max=150)])
    submit = SubmitField('نشر')
