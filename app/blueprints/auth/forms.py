from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('البريد', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    submit = SubmitField('دخول')

class RegisterForm(FlaskForm):
    name = StringField('الاسم', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('البريد', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6)])
    category = SelectField('الفئة', choices=[('طالب','طالب'), ('مدرس','مدرس')], validators=[DataRequired()])
    submit = SubmitField('تسجيل')
