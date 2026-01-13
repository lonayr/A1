from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import CourseForm
from ...extensions import db
from ...models import Course, Enrollment

@courses_bp.route("")
def list():
    q = request.args.get("q", "").strip()
    query = Course.query
    if q:
        query = query.filter(Course.title.ilike(f"%{q}%"))
    items = query.order_by(Course.created_at.desc()).all()
    return render_template("courses/list.html", courses=items, q=q)

@courses_bp.route("/<int:course_id>")
def detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template("courses/detail.html", course=course)

@courses_bp.route("/new", methods=["GET","POST"])
@login_required
def new():
    if current_user.category.name != "مدرس" and not current_user.is_developer:
        flash("هذه الصفحة مخصصة للمدرسين.", "warning")
        return redirect(url_for("index"))
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            image_url=form.image_url.data or None,
            teacher_id=current_user.id
        )
        db.session.add(course); db.session.commit()
        flash("تم نشر الكورس بنجاح.", "success")
        return redirect(url_for("courses.list"))
    return render_template("courses/new.html", form=form)

@courses_bp.route("/<int:course_id>/enroll")
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    exists = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if exists:
        flash("أنت مسجل بالفعل في هذا الكورس.", "info")
    else:
        db.session.add(Enrollment(user_id=current_user.id, course_id=course.id))
        db.session.commit()
        flash("تم التسجيل في الكورس.", "success")
    return redirect(url_for("courses.detail", course_id=course.id))
