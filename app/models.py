from datetime import datetime
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_developer = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('user_cat.id'), nullable=False)
    category = db.relationship('UserCat', backref='users')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self): return True
    @property
    def is_anonymous(self): return False
    def get_id(self): return str(self.id)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher = db.relationship('User', backref='courses')

class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher = db.relationship('User', backref='workshops')

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'))
    user = db.relationship('User', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')
    workshop = db.relationship('Workshop', backref='enrollments')
