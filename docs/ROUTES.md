# 路由與頁面設計 (Routes & Pages)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (任務列表) | GET | `/` | `templates/index.html` | 顯示登入使用者的任務列表；若未登入重導向至登入頁 |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示使用者註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 接收註冊表單，存入 DB，成功後重導向至登入頁 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證帳號密碼，設定 Session，重導向至首頁 |
| 處理登出 | GET | `/auth/logout` | — | 清除 Session，重導向至登入頁 |
| 建立任務 | POST | `/task/add` | — | 接收新增表單，存入 DB，重導向回首頁 |
| 編輯任務 | POST | `/task/<id>/edit` | — | 接收更新表單，更新 DB 中的任務，重導向回首頁 |
| 切換狀態 | POST | `/task/<id>/status` | — | 標記任務為已完成或未完成，重導向回首頁 |
| 刪除任務 | POST | `/task/<id>/delete`| — | 刪除指定任務，重導向回首頁 |

> 註：由於 HTML 表單僅支援 GET 與 POST，故所有的狀態改變（更新、刪除）皆使用 POST 方法。新增與編輯表單則直接放在首頁 (index.html) 或使用彈窗，故沒有獨立的表單頁面路由。

## 2. 每個路由的詳細說明

### Auth 路由 (`/auth`)
- **GET `/auth/register`**
  - 輸入：無
  - 處理邏輯：直接渲染註冊畫面
  - 輸出：`auth/register.html`
- **POST `/auth/register`**
  - 輸入：表單欄位 `username`, `password`
  - 處理邏輯：呼叫 `User.create`，若帳號已存在則回傳錯誤訊息；若成功則重導向
  - 輸出：重導向至 `/auth/login`
- **GET `/auth/login`**
  - 輸入：無
  - 處理邏輯：直接渲染登入畫面
  - 輸出：`auth/login.html`
- **POST `/auth/login`**
  - 輸入：表單欄位 `username`, `password`
  - 處理邏輯：呼叫 `User.get_by_username`，比對 `password_hash`，若正確則設定 `session['user_id']`
  - 輸出：成功重導向至 `/`，失敗則重新渲染帶有錯誤訊息的 `auth/login.html`
- **GET `/auth/logout`**
  - 處理邏輯：清除 `session`
  - 輸出：重導向至 `/auth/login`

### Task 路由 (`/task`)
- **GET `/`** (主頁路由，通常綁在 app.py 或 main blueprint)
  - 處理邏輯：檢查 `session` 是否有 `user_id`。有則呼叫 `Task.get_all_by_user`，否則重導向 `/auth/login`。
  - 輸出：`index.html` 帶入 `tasks` 變數
- **POST `/task/add`**
  - 輸入：表單 `title`, `priority`, `due_date`
  - 處理邏輯：呼叫 `Task.create` 寫入資料庫
  - 輸出：重導向至 `/`
- **POST `/task/<id>/edit`**
  - 輸入：表單 `title`, `priority`, `due_date`
  - 處理邏輯：呼叫 `Task.update` 更新資料
  - 輸出：重導向至 `/`
- **POST `/task/<id>/status`**
  - 輸入：表單 `status`（切換值）
  - 處理邏輯：呼叫 `Task.update_status`
  - 輸出：重導向至 `/`
- **POST `/task/<id>/delete`**
  - 處理邏輯：呼叫 `Task.delete` 刪除資料庫紀錄
  - 輸出：重導向至 `/`

## 3. Jinja2 模板清單

將建立以下模板結構：
- `templates/base.html`：共用的 HTML 骨架（包含 `<head>`、CSS 引入、共用導覽列 Navbar）
- `templates/index.html`：繼承自 `base.html`，顯示任務列表，並包含新增、編輯的表單與刪除按鈕
- `templates/auth/login.html`：繼承自 `base.html`，登入表單頁面
- `templates/auth/register.html`：繼承自 `base.html`，註冊表單頁面

## 4. 路由骨架程式碼
路由骨架已經建立在 `app/routes/` 目錄中，分別為 `auth.py` 與 `task.py`。
