# 快速開始指南

## 🚀 30 分鐘內啟動系統

### 前置需求
- Python 3.10+
- PostgreSQL
- Redis
- Azure Document Intelligence 訂閱
- Azure OpenAI GPT-5 訂閱

---

## 步驟 1: 環境設定 (5 分鐘)

```bash
# 進入專案目錄
cd "/Users/linkaijun/Desktop/EY/台北智慧城市/gov_estimation_system"

# 建立虛擬環境
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

---

## 步驟 2: 配置 .env 檔案 (10 分鐘)

手動建立 `.env` 檔案（複製下方內容並修改）:

```bash
# Azure Document Intelligence
AZURE_DI_ENDPOINT=https://YOUR-RESOURCE.cognitiveservices.azure.com/
AZURE_DI_KEY=YOUR-DI-KEY

# Azure OpenAI GPT-5
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_KEY=YOUR-OPENAI-KEY
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Database (確保 PostgreSQL 已啟動)
DB_NAME=gov_estimation_db
DB_USER=postgres
DB_PASSWORD=YOUR-PASSWORD
DB_HOST=localhost
DB_PORT=5432

# Redis (確保 Redis 已啟動)
REDIS_URL=redis://localhost:6379/0

# Django
SECRET_KEY=請使用隨機生成的密鑰
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Application
MAX_UPLOAD_SIZE_MB=50
ALLOWED_FILE_TYPES=pdf,png,jpg,jpeg,tiff
CONFIDENCE_THRESHOLD=0.7
```

### 生成 SECRET_KEY

```python
# 在 Python 中執行
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 步驟 3: 資料庫設定 (5 分鐘)

```bash
# 建立資料庫（在 PostgreSQL 中執行）
psql -U postgres
CREATE DATABASE gov_estimation_db;
\q

# 執行 Django migrations
cd django_app
python manage.py makemigrations
python manage.py migrate

# 建立超級使用者
python manage.py createsuperuser
```

---

## 步驟 4: 啟動服務 (5 分鐘)

### Terminal 1: 啟動 Django
```bash
cd django_app
python manage.py runserver
```

### Terminal 2: 啟動 Celery Worker
```bash
cd django_app
celery -A django_app worker -l info
```

---

## 步驟 5: 驗證安裝 (5 分鐘)

### 1. 檢查 Django Admin
訪問: http://localhost:8000/admin/
使用剛才建立的超級使用者登入

### 2. 檢查 Health Check
訪問: http://localhost:8000/health/
應該看到 "OK"

### 3. 檢查 API 端點
訪問: http://localhost:8000/api/document/documents/

### 4. 測試文件上傳 (使用 curl)
```bash
curl -X POST http://localhost:8000/api/document/documents/upload/ \
  -F "file=@/path/to/test.pdf" \
  -F "document_type=estimation"
```

---

## 🎉 完成！

系統已經啟動並運行。接下來你可以：

1. **查看文件處理狀態**
   - 訪問 Django Admin: http://localhost:8000/admin/
   - 查看 Documents 和 Processing Logs

2. **準備實際文件範本**
   - 將範例文件放入 `data/sample_documents/`
   - 開始測試與優化

3. **閱讀開發指南**
   - 查看 `DEVELOPMENT_GUIDE.md` 了解如何添加功能
   - 查看 `PROJECT_OVERVIEW.md` 了解專案全貌

---

## 🐛 常見問題

### Q1: 無法連接資料庫
**A**: 確認 PostgreSQL 已啟動
```bash
# macOS
brew services start postgresql

# 檢查狀態
psql -U postgres -c "SELECT 1"
```

### Q2: Redis 連接失敗
**A**: 確認 Redis 已啟動
```bash
# macOS
brew services start redis

# 檢查狀態
redis-cli ping  # 應回應 PONG
```

### Q3: Azure 服務無法連接
**A**: 檢查 .env 中的設定
- 確認 endpoint 格式正確
- 確認 API key 有效
- 確認 GPT-5 deployment name 正確

### Q4: 執行 migrations 出錯
**A**: 刪除現有 migrations 並重新生成
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

---

## 📚 下一步

1. **開發環境設定完成** ✅
2. **準備實際文件範本** ⬅️ 你在這裡
3. **完善 Schema 與 Prompt**
4. **實作驗算規則**
5. **測試與優化**
6. **部署到正式環境**

---

## 🆘 需要幫助？

參考以下文件：
- **README.md** - 基本說明
- **DEVELOPMENT_GUIDE.md** - 開發指南
- **PROJECT_OVERVIEW.md** - 專案總覽
- **TECHNICAL_OVERVIEW.md** - 技術架構

---

*祝開發順利！* 🎊
