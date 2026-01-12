# 開發指南 - 政府估驗計價自動化驗算系統

## 專案結構說明

### 目錄組織

```
gov_estimation_system/
│
├── django_app/                          # Django 應用主目錄
│   ├── apps/                            # 應用模組
│   │   ├── document_processor/          # 文件處理器
│   │   │   ├── models.py                # 資料模型
│   │   │   ├── views.py                 # API 視圖
│   │   │   ├── serializers.py           # 序列化器
│   │   │   ├── tasks.py                 # Celery 異步任務
│   │   │   └── urls.py                  # URL 路由
│   │   │
│   │   └── estimation_validator/        # 估驗計價驗證器
│   │       ├── models.py                # 驗證規則、回饋記錄模型
│   │       ├── views.py                 # 驗證相關 API
│   │       └── ...
│   │
│   ├── services/                        # 服務層（核心業務邏輯）
│   │   ├── base/                        # 基礎服務（可重用）
│   │   │   ├── azure_di_service.py      # Azure Document Intelligence
│   │   │   ├── azure_gpt_service.py     # Azure OpenAI GPT-5
│   │   │   ├── pdf_handler.py           # PDF 處理工具
│   │   │   └── confidence_calculator.py # 信心分數計算
│   │   │
│   │   ├── estimation/                  # 估驗計價專屬服務
│   │   │   ├── amount_engine.py         # 金額驗算引擎
│   │   │   ├── accumulation_checker.py  # 累計檢核模組
│   │   │   ├── payment_condition_engine.py  # 付款條件引擎
│   │   │   └── rules_engine.py          # 規則引擎與學習模組
│   │   │
│   │   └── templates/                   # 模板檔案
│   │       ├── prompt/                  # GPT Prompt 模板
│   │       └── json_format/             # JSON 格式範例
│   │
│   ├── schemas/                         # 資料結構定義
│   │   └── estimation_schema.py         # 估驗計價 JSON Schema
│   │
│   ├── settings/                        # Django 設定
│   │   ├── base.py                      # 基礎設定
│   │   ├── dev.py                       # 開發環境設定
│   │   └── prod.py                      # 正式環境設定
│   │
│   ├── utils/                           # 工具函數
│   │   ├── file_utils.py                # 檔案處理工具
│   │   └── date_utils.py                # 日期處理工具
│   │
│   ├── manage.py                        # Django 管理腳本
│   ├── urls.py                          # 主 URL 配置
│   ├── wsgi.py                          # WSGI 入口
│   └── celery.py                        # Celery 配置
│
├── data/                                # 資料目錄
│   ├── sample_documents/                # 範例文件
│   ├── processed/                       # 處理後的資料
│   ├── results/                         # 驗算結果
│   └── uploads/                         # 上傳文件
│
├── tests/                               # 測試文件
│
├── requirements.txt                     # Python 依賴
├── .gitignore                           # Git 忽略檔案
└── README.md                            # 專案說明
```

---

## 核心模組說明

### 1. 基礎服務層 (services/base/)

#### Azure Document Intelligence Service
- **檔案**: `azure_di_service.py`
- **功能**: ICR 智能字元識別、表格識別、文字擷取
- **狀態**: ✅ 框架完成，TODO: 根據實際 API 版本調整
- **使用方式**:
  ```python
  from django_app.services.base.azure_di_service import get_azure_di_service
  
  di_service = get_azure_di_service()
  result = di_service.analyze_document('path/to/file.pdf')
  ```

#### Azure GPT Service
- **檔案**: `azure_gpt_service.py`
- **功能**: GPT-5 語義理解、欄位對應、邏輯識別
- **狀態**: ✅ 框架完成，配置為 GPT-5
- **使用方式**:
  ```python
  from django_app.services.base.azure_gpt_service import get_azure_gpt_service
  
  gpt_service = get_azure_gpt_service()
  result = gpt_service.process_document(icr_data, prompt_template)
  ```

### 2. 估驗計價專屬服務 (services/estimation/)

#### 金額驗算引擎
- **檔案**: `amount_engine.py`
- **功能**: 
  - 直式加總驗證
  - 橫式計算驗證 (單價 × 數量 = 金額)
  - 小計/總計驗證
- **狀態**: ⚠️ 框架完成，TODO: 待實際文件範本後實作具體規則
- **擴展方式**: 在類別中新增驗證方法

#### 累計檢核模組
- **檔案**: `accumulation_checker.py`
- **功能**:
  - 累計邏輯檢核 (前期累計 + 本期 = 本期累計)
  - 合約總額上限檢查
  - 進度合理性分析
- **狀態**: ⚠️ 框架完成，TODO: 待實際文件範本後實作具體規則

#### 付款條件引擎
- **檔案**: `payment_condition_engine.py`
- **功能**:
  - 自然語言付款條件解析 (使用 GPT)
  - 規則引擎解析 (正則表達式)
  - 付款條件驗證
- **狀態**: ⚠️ 框架完成，TODO: 待實際文件範本後優化

#### 規則引擎與學習模組
- **檔案**: `rules_engine.py`
- **功能**:
  - 規則管理與執行
  - 從回饋中學習
  - 規則自動提取
- **狀態**: ⚠️ 框架完成，TODO: 待有足夠資料後實作學習機制

---

## 開發流程

### 當有實際文件範本後，需要進行的步驟：

#### Phase 1: Schema 完善
1. 分析實際文件結構
2. 更新 `schemas/estimation_schema.py`
3. 確定所有必要欄位

#### Phase 2: Prompt 優化
1. 根據實際文件調整 Prompt
2. 更新 `services/templates/prompt/` 下的模板
3. 進行 Few-shot Learning 範例收集

#### Phase 3: 驗算規則實作
1. 實作金額驗算的具體邏輯
2. 實作累計檢核的具體邏輯
3. 實作付款條件解析的具體規則

#### Phase 4: 測試與優化
1. 使用實際文件進行測試
2. 收集錯誤案例
3. 優化模型與規則

---

## API 端點

### 文件處理 API

```
POST /api/document/documents/upload/
- 上傳文件
- Body: multipart/form-data
  - file: 文件檔案
  - document_type: 文件類型

GET /api/document/documents/
- 取得所有文件列表

GET /api/document/documents/{id}/
- 取得特定文件詳情

GET /api/document/documents/{id}/processing_logs/
- 取得文件處理日誌

POST /api/document/documents/{id}/reprocess/
- 重新處理文件
```

### 驗證 API

```
GET /api/validation/rules/
- 取得所有驗證規則

GET /api/validation/rules/enabled_rules/
- 取得啟用的規則

POST /api/validation/feedback/submit_feedback/
- 提交回饋
```

---

## 環境變數配置

請參考 `.env.example`（如果無法直接創建，請手動建立此檔案）：

```bash
# Azure Document Intelligence
AZURE_DI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_DI_KEY=your-key

# Azure OpenAI GPT-5
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Database
DB_NAME=gov_estimation_db
DB_USER=postgres
DB_PASSWORD=your-password

# Redis
REDIS_URL=redis://localhost:6379/0
```

---

## 待辦事項 (TODO)

### 高優先級
- [ ] 取得實際文件範本
- [ ] 完善 JSON Schema 定義
- [ ] 優化 GPT Prompt 模板
- [ ] 實作具體的驗算規則

### 中優先級
- [ ] 實作規則學習機制
- [ ] 建立測試資料集
- [ ] 前端使用者介面開發
- [ ] API 文件生成

### 低優先級
- [ ] 效能優化
- [ ] 監控與日誌系統
- [ ] 部署腳本
- [ ] 使用者手冊

---

## 貢獻指南

### 程式碼規範
- 使用 Black 進行程式碼格式化
- 使用 Flake8 進行程式碼檢查
- 遵循 PEP 8 規範

### Git 工作流程
1. 從 `main` 分支建立功能分支
2. 在功能分支上開發
3. 提交 Pull Request
4. Code Review 後合併

### 命名規範
- 模組名稱: `snake_case`
- 類別名稱: `PascalCase`
- 函數名稱: `snake_case`
- 常數: `UPPER_CASE`

---

## 聯絡資訊

**專案團隊**: EY 安永  
**技術負責人**: [待填入]  
**客戶單位**: 台北市政府

---

*本文件會隨著專案進展持續更新*
