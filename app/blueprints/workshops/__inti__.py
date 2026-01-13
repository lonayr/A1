from flask import Blueprint
workshops_bp = Blueprint("workshops", __name__, url_prefix="/workshops", template_folder="../../templates/workshops")
from . import routes  # noqa
