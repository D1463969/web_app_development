from flask import render_template, session, redirect, url_for
from app.routes import main_bp
from app.models.task import Task

@main_bp.route('/')
def index():
    """
    首頁路由。
    檢查使用者是否登入，若已登入則取得該使用者的所有任務並渲染 index.html；
    若未登入則重導向至登入頁面。
    """
    pass
