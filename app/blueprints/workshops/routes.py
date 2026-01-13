from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import WorkshopForm
from ...extensions import db
from ...models import Workshop, Enrollment

@workshops_bp.route("")
def list():
    items = Workshop.query.order_by(Workshop.date.desc()).all()
    return render_template("workshops/list.html", workshops=items)

@workshops_bp.route("/<int:ws_id>")
def detail(ws_id):
    ws = Workshop.query.get_or_404(ws_id)
    return render_template("workshops/detail.html", workshop=ws)

@workshops_bp.route("/new", methods=["GET","POST"])
@login_required
def new():
    if current_user.category.name != "مدرس" and not current_user.is_developer:
        flash("هذه الصفحة مخصصة للمدرسين.", "warning")
        return redirect(url_for("index"))
    form = WorkshopForm()
    if form.validate_on_submit():
        ws = Workshop(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            teacher_id=current_user.id
        )
        db.session.add(ws); db.session.commit()
        flash("تم نشر الورشة بنجاح.", "success")
        return redirect(url_for("workshops.list"))
    return render_template("workshops/new.html", form=form)

@workshops_bp.route("/<int:ws_id>/enroll")
@login_required
def enroll(ws_id):
    ws = Workshop.query.get_or_404(ws_id)
    exists = Enrollment.query.filter_by(user_id=current_user.id, workshop_id=ws.id).first()
    if exists:
        flash("أنت مسجل بالفعل في هذه الورشة.", "info")
    else:
        db.session.add(Enrollment(user_id=current_user.id, workshop_id=ws.id))
        db.session.commit()
        flash("تم التسجيل في الورشة.", "success")
    return redirect(url_for("workshops.detail", ws_id=ws.id))
