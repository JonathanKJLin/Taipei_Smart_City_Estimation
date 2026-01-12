# 政府估驗計價自動化驗算系統

## 專案概述
本系統利用 Azure Document Intelligence 和 GPT-5 實現估驗計價文件的智能處理與驗算。

## 技術棧
- Python 3.10+
- Django 4.x
- Azure Document Intelligence
- Azure OpenAI GPT-5
- Celery + Redis
- PostgreSQL

## 目錄結構
```
gov_estimation_system/
├── django_app/                    # Django 應用主目錄
│   ├── apps/                      # 應用模組
│   │   ├── document_processor/    # 文件處理器
│   │   └── estimation_validator/  # 估驗計價驗證器
│   ├── services/                  # 服務層
│   │   ├── base/                  # 基礎服務（Azure、GPT等）
│   │   ├── estimation/            # 估驗計價專屬服務
│   │   ├── validation/            # 驗證服務
│   │   └── templates/             # 模板（Prompt、JSON格式等）
│   ├── schemas/                   # 資料結構定義
│   ├── settings/                  # 配置文件
│   └── utils/                     # 工具函數
├── data/                          # 資料目錄
│   ├── sample_documents/          # 範例文件
│   ├── processed/                 # 處理後的資料
│   ├── results/                   # 驗算結果
│   └── uploads/                   # 上傳文件
└── tests/                         # 測試文件
```

## 快速開始

### 1. 環境設定
```bash
# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### 2. 配置環境變數
複製 `.env.example` 到 `.env` 並填入相關資訊：
```bash
cp .env.example .env
```

### 3. 資料庫遷移
```bash
cd django_app
python manage.py migrate
```

### 4. 啟動服務
```bash
# 啟動 Django 服務
python manage.py runserver

# 啟動 Celery Worker（另開終端）
celery -A django_app worker -l info
```

## 開發狀態

### ✅ 已完成
- 專案架構設計
- 目錄結構建立
- 基礎框架程式碼

### 🚧 待開發（需要實際文件範本後）
- 具體運算規則實作
- 驗算邏輯細節
- Prompt 模板優化
- JSON Schema 細節定義

## 核心功能模組

### 1. 文件處理模組
- Azure DI 文件掃描
- ICR 智能字元識別
- 表格結構識別

### 2. 語義理解模組
- GPT-5 語義分析
- 欄位對應
- 邏輯關聯識別

### 3. AI 規則引擎
- **金額驗算**：加總檢核、橫式計算
- **累計檢核**：前後期累計驗證
- **付款條件**：條件解析與驗算

### 4. 資料標準化
- 結構化 JSON 輸出
- 驗算結果報告
- 信心分數計算

## 開發指南

### 添加新的驗算規則
1. 在 `services/estimation/rules/` 下創建新規則文件
2. 繼承 `BaseRule` 類別
3. 實作 `validate()` 方法
4. 在 `estimation_engine.py` 中註冊規則

### 添加新的文件類型
1. 在 `schemas/` 定義新的 Schema
2. 在 `services/templates/json_format/` 創建 JSON 範本
3. 在 `services/templates/prompt/` 創建對應 Prompt
4. 更新文件處理器路由

## 聯絡資訊
**專案負責人**：EY 團隊  
**客戶單位**：台北市政府

---
*本專案目前處於架構設計階段，具體業務邏輯待實際文件範本後實作。*
