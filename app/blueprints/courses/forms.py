from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, URL

class CourseForm(FlaskForm):
    title = StringField('عنوان الكورس', validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(min=10)])
    image_url = URLField('رابط الصورة', validators=[URL(require_tld=False)], default='')
    submit = SubmitField('نشر')
