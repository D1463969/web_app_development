# 系統架構設計 (Architecture)

## 1. 技術架構說明

本專案是一個基於 Python 的輕量級 Web 應用程式。我們選用以下技術棧來實現任務管理系統：

- **後端框架：Flask**
  - **原因**：Flask 輕量且容易上手，非常適合用來快速打造 MVP 與小型專案。
- **模板引擎：Jinja2**
  - **原因**：內建於 Flask，可直接從後端渲染 HTML 頁面並綁定動態資料，不需架設分離的前端框架（如 React/Vue）。
- **資料庫：SQLite**
  - **原因**：設定零門檻，將資料儲存為單一檔案，非常適合初學者與中小型應用。

### Flask MVC 模式說明
雖然 Flask 本身不強制要求 MVC 模式，但我們將專案架構劃分為：
- **Model（模型）**：負責與 SQLite 資料庫溝通，定義任務（Task）與使用者（User）的資料結構。
- **View（視圖）**：使用 Jinja2 模板引擎生成的 HTML 頁面，負責將資料展示給使用者。
- **Controller（控制器）**：由 Flask 的路由（Routes）擔任，負責接收使用者請求、調用 Model 處理資料，最後將結果交由 View 渲染。

## 2. 專案資料夾結構

本專案採用以下結構，將不同職責的檔案分開，便於維護與開發：

```text
app/
├── models/         ← 資料庫模型 (定義 User 與 Task 的資料表)
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── routes/         ← Flask 路由控制器 (處理 HTTP 請求)
│   ├── __init__.py
│   ├── auth.py     (處理註冊/登入)
│   └── task.py     (處理任務的 CRUD)
├── templates/      ← Jinja2 HTML 模板 (負責前端畫面)
│   ├── base.html   (共用模板)
│   ├── index.html  (任務列表首頁)
│   ├── login.html  (登入頁面)
│   └── register.html (註冊頁面)
└── static/         ← 靜態資源 (CSS、JS、圖片)
    └── style.css
instance/
└── database.db     ← SQLite 資料庫檔案 (自動生成)
app.py              ← 專案入口檔 (負責啟動 Flask 伺服器)
docs/               ← 開發文件 (PRD, 架構圖等)
```

## 3. 元件關係圖

以下圖示呈現使用者、瀏覽器、Flask 與資料庫之間的資料流動關係：

```mermaid
flowchart LR
    Browser([使用者瀏覽器]) <-->|HTTP 請求/回應| Routes[Flask Route (Controller)]
    Routes <-->|查詢/更新資料| Models[Models (資料邏輯)]
    Models <-->|讀寫資料庫| SQLite[(SQLite 資料庫)]
    Routes -->|渲染並傳遞變數| Templates[Jinja2 模板 (View)]
    Templates -->|生成 HTML| Browser
```

## 4. 關鍵設計決策

1. **傳統的 SSR (Server-Side Rendering)**：不採用前後端分離 API，所有資料在後端即透過 Jinja2 渲染完成，這樣可大幅降低初期開發複雜度與跨域(CORS)設定的問題。
2. **藍圖機制 (Flask Blueprints)**：我們將路由分為 `auth` 與 `task`，透過 Blueprint 來管理路由，避免 `app.py` 變得過於龐大，讓程式碼更具擴展性。
3. **Session 驗證**：利用 Flask 內建的 Session 機制來儲存使用者的登入狀態，這比處理 JWT 驗證更為簡單直接，且足以應對當前需求。
