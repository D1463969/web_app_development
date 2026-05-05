import os
import sqlite3
from flask import Flask
from app.routes import auth_bp, task_bp, main_bp

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 載入設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 註冊 Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(main_bp)
    
    return app

app = create_app()

def init_db():
    """初始化資料庫與資料表"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        print("資料庫初始化完成！")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'init_db':
        init_db()
    else:
        # 如果直接執行此檔，則啟動開發伺服器
        app.run(debug=True)
