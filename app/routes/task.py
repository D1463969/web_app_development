from flask import request, redirect, url_for, session, flash
from app.routes import task_bp
from app.models.task import Task
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入後再進行操作。', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@task_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date') or None
    
    if not title:
        flash('任務標題為必填欄位。', 'danger')
        return redirect(url_for('main.index'))
        
    success = Task.create(session['user_id'], title, priority, due_date)
    if success:
        flash('新增任務成功！', 'success')
    else:
        flash('新增任務失敗。', 'danger')
        
    return redirect(url_for('main.index'))

@task_bp.route('/<int:task_id>/edit', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.get_by_id(task_id)
    if not task or task['user_id'] != session['user_id']:
        flash('無權限操作此任務。', 'danger')
        return redirect(url_for('main.index'))
        
    title = request.form.get('title')
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date') or None
    
    if not title:
        flash('任務標題為必填欄位。', 'danger')
        return redirect(url_for('main.index'))
        
    Task.update(task_id, title, priority, due_date)
    flash('更新任務成功！', 'success')
    return redirect(url_for('main.index'))

@task_bp.route('/<int:task_id>/status', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.get_by_id(task_id)
    if not task or task['user_id'] != session['user_id']:
        flash('無權限操作此任務。', 'danger')
        return redirect(url_for('main.index'))
        
    status = request.form.get('status')
    if status in ['Pending', 'Completed']:
        Task.update_status(task_id, status)
        
    return redirect(url_for('main.index'))

@task_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.get_by_id(task_id)
    if not task or task['user_id'] != session['user_id']:
        flash('無權限操作此任務。', 'danger')
        return redirect(url_for('main.index'))
        
    Task.delete(task_id)
    flash('任務已刪除。', 'success')
    return redirect(url_for('main.index'))
