import sqlite3
from app.models.db import get_db_connection

class Task:
    @staticmethod
    def create(user_id, title, priority='Medium', due_date=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO tasks (user_id, title, priority, status, due_date) 
               VALUES (?, ?, ?, 'Pending', ?)''',
            (user_id, title, priority, due_date)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_by_user(user_id):
        conn = get_db_connection()
        tasks = conn.execute(
            'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC', 
            (user_id,)
        ).fetchall()
        conn.close()
        return tasks

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return task

    @staticmethod
    def update(task_id, title, priority, due_date):
        conn = get_db_connection()
        conn.execute(
            '''UPDATE tasks SET title = ?, priority = ?, due_date = ?
               WHERE id = ?''',
            (title, priority, due_date, task_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(task_id, status):
        conn = get_db_connection()
        conn.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (status, task_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
