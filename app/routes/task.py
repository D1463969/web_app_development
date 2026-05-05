from flask import render_template, request, redirect, url_for, session, flash
from app.routes import task_bp
from app.models.task import Task

@task_bp.route('/add', methods=['POST'])
def add_task():
    """
    處理新增任務。
    接收表單資料（標題、優先級、截止日期），並呼叫 Model 存入資料庫，完成後重導向至首頁。
    """
    pass

@task_bp.route('/<int:task_id>/edit', methods=['POST'])
def edit_task(task_id):
    """
    處理編輯任務。
    接收更新後的表單資料，並更新指定 ID 的任務，完成後重導向至首頁。
    """
    pass

@task_bp.route('/<int:task_id>/status', methods=['POST'])
def update_status(task_id):
    """
    處理切換任務狀態（例如：標記為已完成）。
    接收新的狀態值並更新資料庫，完成後重導向至首頁。
    """
    pass

@task_bp.route('/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    處理刪除任務。
    從資料庫中移除指定 ID 的任務，完成後重導向至首頁。
    """
    pass
