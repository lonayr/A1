from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from ...models import Course

@dashboard_bp.route("/student")
@login_required
def student():
    if current_user.category.name != "طالب":
        return redirect(url_for("index"))
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return render_template("dashboard/student.html", courses=courses)

@dashboard_bp.route("/teacher")
@login_required
def teacher():
    if current_user.category.name != "مدرس" and not current_user.is_developer:
        return redirect(url_for("index"))
    my_courses = current_user.courses
    my_workshops = current_user.workshops
    return render_template("dashboard/teacher.html", courses=my_courses, workshops=my_workshops)
