from flask import Blueprint
courses_bp = Blueprint("courses", __name__, url_prefix="/courses", template_folder="../../templates/courses")
from . import routes  # noqa
