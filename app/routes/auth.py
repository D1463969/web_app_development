from flask import render_template, request, redirect, url_for, session, flash
from app.routes import auth_bp
from app.models.user import User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染註冊表單頁面。
    POST: 接收表單資料，建立新帳號並存入資料庫，成功後重導向至登入頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染登入表單頁面。
    POST: 驗證帳號密碼，成功則設定 Session 並重導向至首頁，失敗則顯示錯誤訊息。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    處理使用者登出，清除 Session 並重導向至登入頁面。
    """
    pass
