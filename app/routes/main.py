from flask import render_template, session, redirect, url_for
from app.routes import main_bp
from app.models.task import Task

@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    tasks = Task.get_all_by_user(session['user_id'])
    return render_template('index.html', tasks=tasks)
