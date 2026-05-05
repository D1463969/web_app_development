from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import auth_bp
from app.models.user import User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請填寫帳號與密碼。', 'danger')
            return redirect(url_for('auth.register'))
            
        password_hash = generate_password_hash(password)
        success = User.create(username, password_hash)
        
        if success:
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('此帳號已存在，請更換帳號名稱。', 'danger')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請填寫帳號與密碼。', 'danger')
            return redirect(url_for('auth.login'))
            
        user = User.get_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('main.index'))
        else:
            flash('帳號或密碼錯誤。', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('您已成功登出。', 'success')
    return redirect(url_for('auth.login'))
