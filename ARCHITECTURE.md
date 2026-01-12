# 系統架構文檔

> 政府估驗計價自動化驗算系統 - 技術架構與設計

---

## 📐 系統架構概覽

```
┌─────────────────────────────────────────────────────────────────┐
│                      估驗計價文件輸入層                           │
│  (PDF/Image格式的估驗計價單、付款明細、工程合約等)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              文件掃描與 ICR 層 (Azure DI)                         │
│  • 文件分類識別                                                   │
│  • 表格結構辨識                                                   │
│  • 文字、數字、欄位擷取（智能字元識別）                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           自然語言處理與理解層 (GPT-5)                            │
│  • 欄位語義理解與對應                                             │
│  • 邏輯關聯識別（加總關係、條件關係）                              │
│  • 付款條件描述解析                                               │
│  • 數據標準化處理                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  AI 規則引擎核心層                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ 金額加總模組 │  │ 累計檢核模組 │  │ 條件驗算模組 │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  • 自動執行驗算邏輯                                               │
│  • 錯誤偵測與標記                                                 │
│  • 規則動態學習與優化                                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              資料輸出與回饋層                                     │
│  • 標準化 JSON 格式輸出                                           │
│  • 驗算結果報告                                                   │
│  • 異常標記與建議                                                 │
│  • 人工審核介面                                                   │
│  • 回饋機制（強化學習）                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 核心模組詳解

### 1. 文件處理模組 (Document Processing)

**功能**：接收並預處理各類文件

**技術棧**：
- Azure Document Intelligence API
- PyPDF2 / pdf2image

**處理流程**：
```python
# services/base/azure_di_service.py
class AzureDocumentIntelligenceService:
    def analyze_document(file_path, model_id="prebuilt-layout"):
        # ICR 智能字元識別
        # 表格結構辨識
        # 返回結構化資料
        return structured_data
```

### 2. 語義理解模組 (Semantic Understanding)

**功能**：使用 GPT-5 理解文件語義

**核心能力**：
- 欄位對應到標準 Schema
- 識別邏輯關聯（如：單價 × 數量 = 金額）
- 解析付款條件自然語言

**實作**：
```python
# services/base/azure_gpt_service.py
class AzureGPTService:
    def understand_field_mapping(icr_data, target_schema):
        # Few-shot Learning + Prompt Engineering
        # 返回標準化資料
        return mapped_data
```

### 3. AI 規則引擎 (Rules Engine)

#### 3.1 金額驗算引擎

**驗證項目**：
- ✅ 直式加總：所有項目金額加總 = 總金額
- ✅ 橫式計算：單價 × 數量 = 金額
- ✅ 小計與總計檢核

**實作架構**：
```python
# services/estimation/amount_engine.py
class AmountCalculationEngine:
    def validate_vertical_sum(data):
        # 驗證直式加總
        
    def validate_horizontal_calculation(data):
        # 驗證橫式計算
```

#### 3.2 累計檢核模組

**驗證邏輯**：
```
前期累計 + 本期金額 = 本期累計
本期累計 ≤ 合約總額
```

**實作架構**：
```python
# services/estimation/accumulation_checker.py
class AccumulationChecker:
    def check_accumulation_logic(current, previous):
        # 驗證累計邏輯
        
    def check_contract_limit(current, contract):
        # 驗證合約上限
```

#### 3.3 付款條件引擎

**功能**：
- 解析自然語言付款條件（使用 GPT-5）
- 驗證是否符合付款條件

**範例**：
```
輸入：「工程完成30%後支付第二期款」
輸出：{
  "trigger_type": "progress",
  "threshold": 30,
  "payment_phase": 2
}
```

---

## 💾 資料流程

### 完整處理流程

```
1. 文件上傳
   ↓
2. Azure DI ICR 掃描
   ↓
3. 初步資料擷取（表格、文字、數字）
   ↓
4. GPT-5 語義分析與欄位對應
   ↓
5. 資料標準化處理
   ↓
6. AI 規則引擎驗算
   ├─ 金額加總檢查
   ├─ 累計金額檢核
   └─ 付款條件驗算
   ↓
7. 生成標準化 JSON 輸出
   ↓
8. 驗算結果報告與異常標記
   ↓
9. 人工審核與回饋
   ↓
10. AI 模組持續優化
```

### 資料格式範例

**輸入：Azure DI ICR 掃描結果**
```json
{
  "pages": [{
    "tables": [{
      "cells": [
        {"row": 0, "col": 0, "content": "項次"},
        {"row": 1, "col": 1, "content": "鋼筋工程"}
      ]
    }],
    "key_value_pairs": [...],
    "text": "..."
  }]
}
```

**輸出：標準化估驗計價資料**
```json
{
  "document_type": "估驗計價單",
  "document_id": "EST-2026-001",
  "period_number": 3,
  "contract_info": {
    "contract_number": "1100-A123",
    "contract_amount": 50000000
  },
  "items": [
    {
      "item_no": "1",
      "description": "鋼筋工程",
      "unit": "噸",
      "quantity": 120.5,
      "unit_price": 25000,
      "amount": 3012500
    }
  ],
  "validation_results": {
    "amount_validation": {"status": "pass"},
    "accumulation_validation": {"status": "pass"},
    "payment_condition_validation": {"status": "pass"}
  },
  "confidence_scores": {
    "overall": 0.92,
    "icr_accuracy": 0.95,
    "field_mapping": 0.90
  }
}
```

---

## 🏗️ 技術架構

### 後端架構

```
Django 4.x (Web Framework)
    │
    ├─ REST API (DRF)
    │   ├─ Document Upload
    │   ├─ Processing Status
    │   └─ Validation Results
    │
    ├─ Celery (Async Tasks)
    │   ├─ Document Processing
    │   ├─ ICR Analysis
    │   └─ Validation Tasks
    │
    ├─ Services Layer
    │   ├─ Azure DI Service
    │   ├─ Azure GPT Service
    │   └─ Validation Services
    │
    └─ Data Layer
        ├─ PostgreSQL (主資料庫)
        └─ Redis (快取 + 任務佇列)
```

### 部署架構

```
┌─────────────┐
│  Azure LB   │  負載平衡
└──────┬──────┘
       │
   ┌───┴───┬───────┬───────┐
   │       │       │       │
┌──▼──┐ ┌──▼──┐ ┌──▼──┐ ┌──▼──┐
│Django│ │Django│ │Django│ │Django│
│ App  │ │ App  │ │ App  │ │ App  │
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘
   │        │        │        │
   └────────┼────────┴────────┘
            │
    ┌───────┴───────┐
    │               │
┌───▼───┐     ┌─────▼─────┐
│ Redis │     │PostgreSQL │
└───┬───┘     └───────────┘
    │
┌───▼────┐
│ Celery │
│Workers │
└───┬────┘
    │
┌───▼──────────────┐
│  Azure Services  │
│ • Document Intel │
│ • OpenAI GPT-5   │
│ • Blob Storage   │
└──────────────────┘
```

---

## 🔐 安全性設計

### 安全層級

| 層級 | 措施 |
|------|------|
| **傳輸安全** | HTTPS/TLS 加密 |
| **資料安全** | AES-256 加密儲存 |
| **身份驗證** | OAuth 2.0 + JWT |
| **權限控制** | RBAC 角色權限管理 |
| **稽核日誌** | 完整操作記錄 |
| **資料遮罩** | 敏感資訊保護 |

### Django 安全設定

```python
# settings/prod.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## ⚡ 效能指標

| 指標 | 目標值 | 說明 |
|------|--------|------|
| **文件處理時間** | < 5 分鐘 | 從上傳到完成驗算 |
| **ICR 準確率** | > 95% | Azure DI 智能字元識別 |
| **欄位對應準確率** | > 90% | GPT 語義理解 |
| **驗算準確率** | > 98% | 規則引擎計算 |
| **整體信心分數** | > 85% | 綜合評估 |
| **並發處理** | 50+ 文件 | 同時處理能力 |

---

## 📊 資料庫設計

### 核心 Models

**Document**（文件）
```python
- document_id: 文件編號
- document_type: 文件類型
- file_path: 檔案路徑
- status: 處理狀態
- icr_result: ICR 結果
- structured_data: 結構化資料
- validation_result: 驗算結果
- confidence_score: 信心分數
```

**ValidationRule**（驗證規則）
```python
- rule_id: 規則 ID
- rule_name: 規則名稱
- rule_type: 規則類型
- rule_config: 規則配置
- enabled: 是否啟用
```

**FeedbackRecord**（回饋記錄）
```python
- document_id: 文件編號
- field_name: 欄位名稱
- system_value: 系統值
- correct_value: 正確值
- feedback_type: 回饋類型
```

---

## 🔄 擴展性設計

### 橫向擴展
- Django 應用無狀態設計
- Celery Worker 可任意擴展
- 負載平衡支援

### 垂直擴展
- 資料庫讀寫分離
- Redis Cluster
- 快取策略優化

### 功能擴展
- 模組化設計
- Plugin 架構
- API 版本控制

---

## 🎯 GPT-5 配置

### 環境變數
```bash
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### 服務初始化
```python
# services/base/azure_gpt_service.py
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=settings.AZURE_OPENAI_KEY,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
)
```

### Prompt Engineering
- Few-shot Learning 範例
- 結構化輸出指引
- JSON Schema 驗證

---

## 📈 監控與日誌

### 日誌層級
- **DEBUG**: 開發除錯資訊
- **INFO**: 一般操作記錄
- **WARNING**: 警告訊息
- **ERROR**: 錯誤事件
- **CRITICAL**: 嚴重錯誤

### 監控指標
- API 回應時間
- Celery 任務狀態
- 資料庫查詢效能
- Azure 服務調用次數
- 記憶體與 CPU 使用率

---

## 🚀 未來規劃

### Phase 2
- [ ] 前端使用者介面
- [ ] 批次處理功能
- [ ] 報表生成系統

### Phase 3
- [ ] 行動端 App
- [ ] 跨機關資料整合
- [ ] 預警系統

### Phase 4
- [ ] AI 模型微調
- [ ] 自動化測試框架
- [ ] 效能優化

---

*最後更新: 2026-01-12*  
*版本: 1.0.0*
