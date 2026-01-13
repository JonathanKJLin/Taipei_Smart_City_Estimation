# 政府估驗計價自動化驗算系統

> 利用 Azure Document Intelligence (ICR) 和 GPT-5 實現估驗計價文件的智能處理與自動驗算

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)
[![Azure](https://img.shields.io/badge/Azure-AI%20Services-0078D4.svg)](https://azure.microsoft.com/)
[![GPT-5](https://img.shields.io/badge/OpenAI-GPT--5-412991.svg)](https://openai.com/)

---

## 專案概述

本系統為台北市政府開發的智能化估驗計價文件處理與驗算平台，透過 AI 技術實現：

- **智能字元識別 (ICR)**：使用 Azure Document Intelligence 掃描與識別文件
- **語義理解**：利用 GPT-5 理解欄位邏輯與付款條件
- **自動驗算**：金額加總、累計檢核、付款條件驗證
- **標準化輸出**：結構化 JSON 格式資料
- **持續學習**：透過回饋機制優化 AI 模型

---

## 核心功能

### 1. 文件處理
- Azure DI ICR 智能字元識別
- 表格結構自動辨識
- 多格式文件支援 (PDF, 圖片)

### 2. AI 規則引擎
- **金額驗算**：直式加總、橫式計算 (單價×數量=金額)
- **累計檢核**：前期累計 + 本期 = 本期累計
- **付款條件**：自然語言條件解析與驗證

### 3. 智能學習
- 自動提取驗算規則
- 從回饋中持續優化
- 動態調整驗算邏輯

---

## 快速開始

### 前置需求
- Python 3.10+
- PostgreSQL
- Redis
- Azure Document Intelligence 訂閱
- Azure OpenAI GPT-5 訂閱

### 步驟 1: 環境設定

```bash
# 克隆專案
git clone https://github.com/JonathanKJLin/-.git
cd gov_estimation_system

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### 步驟 2: 配置環境變數

複製 `env.example` 並根據你的環境修改：

```bash
# Azure Document Intelligence
AZURE_DI_ENDPOINT=https://YOUR-RESOURCE.cognitiveservices.azure.com/
AZURE_DI_KEY=YOUR-DI-KEY

# Azure OpenAI GPT-5
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_KEY=YOUR-OPENAI-KEY
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Database
DB_NAME=gov_estimation_db
DB_USER=postgres
DB_PASSWORD=YOUR-PASSWORD

# Redis
REDIS_URL=redis://localhost:6379/0
```

生成 Django SECRET_KEY：
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 步驟 3: 資料庫設定

```bash
# 建立資料庫
psql -U postgres
CREATE DATABASE gov_estimation_db;
\q

# 執行 migrations
cd django_app
python manage.py makemigrations
python manage.py migrate

# 建立管理員帳號
python manage.py createsuperuser
```

### 步驟 4: 啟動服務

**Terminal 1 - Django Server:**
```bash
cd django_app
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
cd django_app
celery -A django_app worker -l info
```

### 步驟 5: 驗證安裝

- **Django Admin**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/
- **API Documentation**: http://localhost:8000/api/

測試文件上傳：
```bash
curl -X POST http://localhost:8000/api/document/documents/upload/ \
  -F "file=@test.pdf" \
  -F "document_type=estimation"
```

---

## 專案結構

```
gov_estimation_system/
├── django_app/                    # Django 應用
│   ├── apps/                      
│   │   ├── document_processor/    # 文件處理器
│   │   └── estimation_validator/  # 驗證器
│   ├── services/                  
│   │   ├── base/                  # 基礎服務 (Azure DI, GPT)
│   │   ├── estimation/            # 驗算引擎
│   │   └── templates/             # Prompt 模板
│   ├── schemas/                   # JSON Schema
│   ├── settings/                  # 配置 (dev/prod)
│   └── utils/                     # 工具函數
├── data/                          # 資料目錄
│   ├── sample_documents/          # 範例文件
│   ├── uploads/                   # 上傳文件
│   └── results/                   # 驗算結果
└── tests/                         # 測試
```

---

## 文檔

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - 系統架構與技術細節
- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)** - 開發指南與 API 文檔

---

## 開發狀態

### 已完成
- 完整的 Django 應用架構
- Azure DI + GPT-5 服務整合
- 三大驗算引擎框架
- 文件處理與異步任務
- 完整的文檔體系

### 待完成（需實際文件範本）
- 具體驗算規則實作
- Prompt 模板優化
- JSON Schema 細節調整
- 規則學習機制訓練

---

## 常見問題

<details>
<summary><b>Q1: 無法連接 PostgreSQL</b></summary>

```bash
# 確認 PostgreSQL 已啟動
brew services start postgresql  # macOS
psql -U postgres -c "SELECT 1"
```
</details>

<details>
<summary><b>Q2: Redis 連接失敗</b></summary>

```bash
# 確認 Redis 已啟動
brew services start redis  # macOS
redis-cli ping  # 應回應 PONG
```
</details>

<details>
<summary><b>Q3: Azure 服務無法連接</b></summary>

檢查 `.env` 設定：
- Endpoint 格式是否正確
- API Key 是否有效
- GPT-5 Deployment Name 是否正確
</details>

---

## 貢獻指南

### 程式碼規範
- 使用 Black 格式化: `black .`
- 使用 Flake8 檢查: `flake8 .`
- 遵循 PEP 8 規範

### Git 工作流程
1. Fork 本專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## 技術棧

| 類別 | 技術 |
|------|------|
| **後端框架** | Django 4.x, Django REST Framework |
| **AI 服務** | Azure Document Intelligence, Azure OpenAI GPT-5 |
| **異步處理** | Celery, Redis |
| **資料庫** | PostgreSQL |
| **文件處理** | PyPDF2, pdf2image |
| **資料處理** | Pandas, NumPy |

---

## 授權

本專案為 EY 安永聯合會計師事務所為台北市政府開發。

---

## 聯絡方式

**專案負責人**: EY 團隊  
**客戶單位**: 台北市政府  
**GitHub**: [https://github.com/JonathanKJLin/-](https://github.com/JonathanKJLin/-)

---

## 路線圖

- [x] 專案架構設計
- [x] 基礎服務整合
- [x] 驗算引擎框架
- [ ] 實際文件範本收集
- [ ] 驗算規則實作
- [ ] 前端介面開發
- [ ] 測試與優化
- [ ] 正式部署

---

*專案當前處於架構設計階段，具體業務邏輯待實際文件範本後實作。*
