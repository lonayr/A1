from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from ...extensions import db
from ...models import User, UserCat

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("تم تسجيل الدخول.", "success")
            if user.category.name == "طالب":
                return redirect(url_for("dashboard.student"))
            elif user.category.name == "مدرس":
                return redirect(url_for("dashboard.teacher"))
            return redirect(url_for("index"))
        flash("بيانات الدخول غير صحيحة.", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        cat = UserCat.query.filter_by(name=form.category.data).first()
        user = User(name=form.name.data, email=form.email.data, is_active=True, category_id=cat.id)
        user.set_password(form.password.data)
        db.session.add(user); db.session.commit()
        flash("تم التسجيل بنجاح. يمكنك تسجيل الدخول الآن.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج.", "info")
    return redirect(url_for("index"))
