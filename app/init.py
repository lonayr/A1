from flask import Flask
from .config import Config
from .extensions import db, login_manager, migrate
from .models import UserCat, User
from .blueprints.auth import auth_bp
from .blueprints.courses import courses_bp
from .blueprints.workshops import workshops_bp
from .blueprints.dashboard import dashboard_bp

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "الرجاء تسجيل الدخول للوصول."

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(workshops_bp)
    app.register_blueprint(dashboard_bp)

    @app.before_first_request
    def bootstrap():
        for name in ["مدير", "مدرس", "طالب"]:
            if not UserCat.query.filter_by(name=name).first():
                db.session.add(UserCat(name=name, description=f"تصنيف {name}"))
        db.session.commit()
        if not User.query.filter_by(email="dev@edu.local").first():
            dev_cat = UserCat.query.filter_by(name="مدير").first()
            dev = User(name="المطور", email="dev@edu.local", is_developer=True, is_active=True, category_id=dev_cat.id)
            dev.set_password("Dev123!")
            db.session.add(dev); db.session.commit()

    @app.route("/")
    def index():
        from .models import Course, Workshop
        courses = Course.query.order_by(Course.created_at.desc()).limit(8).all()
        workshops = Workshop.query.order_by(Workshop.date.desc()).limit(6).all()
        return flask.render_template("index.html", courses=courses, workshops=workshops)

    return app
