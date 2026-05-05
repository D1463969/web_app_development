import sqlite3
from app.models.db import get_db_connection

class User:
    """
    使用者 Model，處理 users 資料表的存取。
    """

    @staticmethod
    def create(username, password_hash):
        """
        新增一位使用者。
        :param username: 使用者帳號
        :param password_hash: 加密後的密碼
        :return: 建立成功回傳 True，若帳號已存在或發生錯誤回傳 False
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 捕捉 UNIQUE constraint failed (帳號已存在)
            return False
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        根據 ID 取得使用者。
        :param user_id: 使用者 ID
        :return: 回傳 sqlite3.Row 或 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return user
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_username(username):
        """
        根據帳號取得使用者。
        :param username: 使用者帳號
        :return: 回傳 sqlite3.Row 或 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            return user
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()
