import sqlite3
from app.models.db import get_db_connection

class Task:
    """
    任務 Model，處理 tasks 資料表的存取。
    """

    @staticmethod
    def create(user_id, title, priority='Medium', due_date=None):
        """
        新增一筆任務。
        :param user_id: 擁有此任務的使用者 ID
        :param title: 任務標題
        :param priority: 優先級 (High/Medium/Low)
        :param due_date: 截止日期 (YYYY-MM-DD字串)
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO tasks (user_id, title, priority, status, due_date) 
                   VALUES (?, ?, ?, 'Pending', ?)''',
                (user_id, title, priority, due_date)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating task: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all_by_user(user_id):
        """
        取得特定使用者的所有任務，按建立時間反序排列。
        :param user_id: 使用者 ID
        :return: list of sqlite3.Row
        """
        try:
            conn = get_db_connection()
            tasks = conn.execute(
                'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC', 
                (user_id,)
            ).fetchall()
            return tasks
        except Exception as e:
            print(f"Error getting tasks for user: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(task_id):
        """
        根據 ID 取得單筆任務。
        :param task_id: 任務 ID
        :return: sqlite3.Row 或 None
        """
        try:
            conn = get_db_connection()
            task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
            return task
        except Exception as e:
            print(f"Error getting task by id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(task_id, title, priority, due_date):
        """
        更新任務內容。
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                '''UPDATE tasks SET title = ?, priority = ?, due_date = ?
                   WHERE id = ?''',
                (title, priority, due_date, task_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update_status(task_id, status):
        """
        更新任務狀態（Pending/Completed）。
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE tasks SET status = ? WHERE id = ?',
                (status, task_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating task status: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(task_id):
        """
        刪除特定任務。
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
