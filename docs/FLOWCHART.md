# 流程圖設計 (Flowchart)

根據 PRD 與系統架構，以下是本任務管理系統的流程與操作路徑設計。

## 1. 使用者流程圖 (User Flow)

這張流程圖展示了使用者進入網站後，可能進行的所有主要操作路徑。

```mermaid
flowchart LR
    Start([使用者進入網站]) --> CheckLogin{是否已登入？}
    
    CheckLogin -->|否| LoginPage[登入頁面]
    LoginPage -->|沒有帳號| RegisterPage[註冊頁面]
    RegisterPage -->|註冊成功| LoginPage
    LoginPage -->|登入成功| HomePage
    
    CheckLogin -->|是| HomePage[首頁 - 任務列表]
    
    HomePage --> Action{要執行什麼操作？}
    
    Action -->|點擊「新增」| AddForm[填寫新增任務表單]
    AddForm -->|送出表單| HomePage
    
    Action -->|點擊「完成」| MarkDone[更新狀態為已完成]
    MarkDone --> HomePage
    
    Action -->|點擊「編輯」| EditForm[填寫編輯任務表單]
    EditForm -->|送出更新| HomePage
    
    Action -->|點擊「刪除」| DeleteTask[刪除該任務]
    DeleteTask --> HomePage
    
    Action -->|點擊「登出」| Logout[清除 Session]
    Logout --> LoginPage
```

## 2. 系統序列圖 (Sequence Diagram)

以「使用者新增一個任務」為例，展示後端各元件如何協作。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route (Controller)
    participant Model as Task Model
    participant DB as SQLite 資料庫

    User->>Browser: 在首頁填寫任務內容並點擊「新增」
    Browser->>Route: POST /task/add (攜帶表單資料)
    
    Route->>Route: 驗證使用者是否已登入
    Route->>Model: 呼叫建立任務邏輯
    Model->>DB: INSERT INTO tasks (title, status, user_id...)
    DB-->>Model: 回傳成功
    Model-->>Route: 建立完成
    
    Route-->>Browser: HTTP 302 重導向回首頁 (GET /)
    Browser->>Route: GET /
    Route->>Model: 查詢使用者的任務列表
    Model->>DB: SELECT * FROM tasks WHERE user_id = ?
    DB-->>Model: 回傳任務資料
    Model-->>Route: 任務列表清單
    Route->>Browser: 渲染 index.html (包含最新任務清單)
    Browser-->>User: 畫面更新，看到新任務
```

## 3. 功能清單與路由對照表

規劃後端應該提供的 URL 節點與 HTTP 方法對應：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| -------- | -------- | --------- | ---- |
| 首頁與任務列表 | `/` | `GET` | 渲染首頁，並顯示登入使用者的任務列表 |
| 使用者註冊 | `/auth/register` | `GET`, `POST` | 渲染註冊表單 (`GET`) 與處理註冊邏輯 (`POST`) |
| 使用者登入 | `/auth/login` | `GET`, `POST` | 渲染登入表單 (`GET`) 與處理登入邏輯 (`POST`) |
| 使用者登出 | `/auth/logout` | `GET` | 清除使用者 Session，跳回登入頁面 |
| 新增任務 | `/task/add` | `POST` | 接收表單資料，建立新任務，並重導向回首頁 |
| 編輯任務 | `/task/edit/<id>` | `POST` | 更新特定 ID 的任務內容，並重導向回首頁 |
| 更新任務狀態 | `/task/status/<id>` | `POST` | 將任務切換為已完成/未完成，並重導向回首頁 |
| 刪除任務 | `/task/delete/<id>` | `POST` | 刪除特定 ID 的任務，並重導向回首頁 |
