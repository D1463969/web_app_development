from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
task_bp = Blueprint('task', __name__, url_prefix='/task')
main_bp = Blueprint('main', __name__)

from . import auth, task, main
