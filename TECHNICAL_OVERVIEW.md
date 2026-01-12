# 智慧城市估驗計價系統 - 技術概覽速查

## 🎯 一句話描述
> 利用 **Azure Document Intelligence** 掃描估驗計價文件，透過 **GPT-4** 理解邏輯關聯，建立 **AI 規則引擎**自動執行金額驗算與檢核，輸出標準化 JSON 並持續優化。

---

## 📊 系統架構圖

```
┌─────────────┐
│  文件上傳   │  PDF/Image 格式的估驗計價相關文件
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│          Azure Document Intelligence            │
│  ┌──────────────┐  ┌──────────────────────┐    │
│  │ Form Recog.  │  │   Layout Analysis    │    │
│  │   (ICR)      │  │   (Table Extract)    │    │
│  └──────────────┘  └──────────────────────┘    │
│         ICR 智能字元識別 + 表格結構識別          │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
                   JSON
        {text, tables, fields, ...}
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│            Azure OpenAI GPT-4/4o                │
│  ┌────────────────────────────────────────┐    │
│  │   Few-shot Prompt Engineering          │    │
│  │   • 欄位語義對應                        │    │
│  │   • 邏輯關聯識別                        │    │
│  │   • 付款條件解析                        │    │
│  └────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
            標準化 JSON 資料
  {項目, 單價, 數量, 金額, 累計, ...}
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│            AI 規則引擎 (Python)                  │
│  ┌───────────────┐ ┌───────────────┐          │
│  │ 金額加總模組  │ │ 累計檢核模組  │          │
│  │ • 直式加總    │ │ • 前期+本期   │          │
│  │ • 橫式加總    │ │ • 合約上限    │          │
│  │ • 小計/總計   │ │ • 異常偵測    │          │
│  └───────────────┘ └───────────────┘          │
│  ┌───────────────────────────────────┐        │
│  │    付款條件驗算模組                │        │
│  │    • 條件解析 (NLP)               │        │
│  │    • 進度比對                      │        │
│  │    • 付款比例檢核                  │        │
│  └───────────────────────────────────┘        │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
              驗算結果報告
    ┌──────────────────────────┐
    │  ✓ PASS 項目             │
    │  ✗ FAIL 項目 (含說明)    │
    │  ⚠ WARNING 項目          │
    │  📊 信心分數             │
    └────────┬─────────────────┘
             │
             ▼
    ┌────────────────────┐
    │   人工審核介面      │
    │   • 確認結果        │
    │   • 標記錯誤        │
    │   • 提供回饋        │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │   回饋學習機制      │
    │   • 規則庫更新      │
    │   • 模型微調        │
    │   • 持續優化        │
    └────────────────────┘
```

---

## 🔧 核心技術組合

### 雲端 AI 服務
```
Azure Document Intelligence  →  文件掃描與 ICR（智能字元識別）
Azure OpenAI GPT-4          →  NLP 語義理解
Azure Blob Storage          →  文件儲存
```

### 應用框架
```
Django 4.x      →  Web 框架
Celery          →  異步任務處理
Redis           →  快取與訊息佇列
PostgreSQL      →  主資料庫
```

### Python 套件
```
openai          →  OpenAI API 整合
azure-ai-*      →  Azure 服務整合
pandas          →  資料處理
PyPDF2          →  PDF 處理
```

---

## 💻 關鍵程式模組

### 1. 文件處理服務
```python
# services/base/azure_service.py
class AzureDocumentService:
    def extract_document(self, file_path):
        """使用 Azure DI 擷取文件內容"""
        # ICR 智能字元識別 + 表格識別
        return structured_data
```

### 2. GPT 語義處理
```python
# services/base/azure_gpt_processor.py
class GPTProcessor:
    def understand_logic(self, icr_data, prompt_template):
        """使用 GPT 理解文件邏輯"""
        # 欄位對應 + 邏輯識別
        return standardized_json
```

### 3. 金額驗算引擎
```python
# services/estimation/amount_engine.py
class AmountCalculationEngine:
    def validate_vertical_sum(self, items):
        """驗證直式加總"""
        calculated = sum([item['amount'] for item in items])
        declared = items.get('total')
        return calculated == declared
    
    def validate_horizontal_calculation(self, item):
        """驗證橫式計算 (單價 × 數量 = 金額)"""
        return item['unit_price'] * item['quantity'] == item['amount']
```

### 4. 累計檢核模組
```python
# services/estimation/accumulation_checker.py
class AccumulationChecker:
    def check_accumulation_logic(self, current_period, previous_periods):
        """檢核累計邏輯"""
        prev_total = previous_periods[-1].get('累計金額', 0)
        current_amount = current_period.get('本期金額')
        current_total = current_period.get('本期累計')
        
        return prev_total + current_amount == current_total
```

### 5. 付款條件引擎
```python
# services/estimation/payment_condition_engine.py
class PaymentConditionEngine:
    def parse_condition(self, condition_text):
        """解析付款條件 (使用 GPT)"""
        # "工程完成30%後支付第二期款" → 結構化規則
        return structured_condition
    
    def validate_payment(self, condition, actual_data):
        """驗證付款是否符合條件"""
        return validation_result
```

---

## 📄 JSON Schema 範例

### 輸入：Azure DI ICR 掃描結果
```json
{
  "pages": [
    {
      "tables": [
        {
          "cells": [
            {"row": 0, "col": 0, "content": "項次"},
            {"row": 0, "col": 1, "content": "項目名稱"},
            {"row": 1, "col": 1, "content": "鋼筋工程"}
          ]
        }
      ],
      "key_value_pairs": [...],
      "text": "..."
    }
  ]
}
```

### 輸出：標準化估驗計價資料
```json
{
  "document_type": "估驗計價單",
  "document_id": "EST-2026-001",
  "contract_info": {
    "contract_number": "1100-A123",
    "contract_amount": 50000000,
    "contractor": "ABC營造股份有限公司"
  },
  "current_period": {
    "period_number": 3,
    "items": [
      {
        "item_no": "1",
        "description": "鋼筋工程",
        "unit": "噸",
        "quantity": 120.5,
        "unit_price": 25000,
        "amount": 3012500,
        "previous_quantity": 250.0,
        "total_quantity": 370.5
      }
    ],
    "period_amount": 3012500,
    "previous_accumulation": 15000000,
    "current_accumulation": 18012500
  },
  "validation_results": {
    "amount_validation": {
      "vertical_sum": {"status": "pass", "message": ""},
      "horizontal_calc": {"status": "pass", "message": ""},
      "subtotal_check": {"status": "pass", "message": ""}
    },
    "accumulation_validation": {
      "logic_check": {"status": "pass", "message": ""},
      "contract_limit": {"status": "pass", "message": ""},
      "progress_check": {"status": "warning", "message": "進度略快於預期"}
    },
    "payment_condition_validation": {
      "condition": "工程完成35%後可請領第三期款",
      "actual_progress": 36.025,
      "status": "pass",
      "message": "符合付款條件"
    }
  },
  "confidence_scores": {
    "overall": 0.92,
    "icr_accuracy": 0.95,
    "field_mapping": 0.90,
    "logic_understanding": 0.91
  },
  "flags": [
    {"type": "info", "message": "本期累計已達合約金額36%"}
  ],
  "processed_timestamp": "2026-01-12T10:30:00Z"
}
```

---

## 🔄 處理流程時序圖

```
使用者          系統          Azure DI       Azure GPT      規則引擎
  │              │               │              │              │
  ├─上傳PDF──────>│               │              │              │
  │              ├─呼叫 ICR────────>│              │              │
  │              │               ├─掃描文件      │              │
  │              │               ├─識別表格      │              │
  │              │<──回傳結構資料──┤              │              │
  │              │               │              │              │
  │              ├─呼叫 GPT─────────────────────>│              │
  │              │               │              ├─理解語義      │
  │              │               │              ├─對應欄位      │
  │              │               │              ├─識別邏輯      │
  │              │<─────────────────回傳標準JSON──┤              │
  │              │               │              │              │
  │              ├─執行驗算────────────────────────────────────>│
  │              │               │              │              ├─金額加總
  │              │               │              │              ├─累計檢核
  │              │               │              │              ├─條件驗算
  │              │<─────────────────────────────────驗算結果────┤
  │              │               │              │              │
  │<─顯示結果────┤               │              │              │
  │              │               │              │              │
  ├─審核&回饋───>│               │              │              │
  │              ├─更新規則庫────>│              │              │
  │              │               │              │              │
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

---

## 🔐 安全性設計

```
┌─────────────────────────────────────┐
│         安全層級                     │
├─────────────────────────────────────┤
│ 1. 傳輸加密 (HTTPS/TLS)             │
│ 2. 資料加密 (AES-256)               │
│ 3. 身份驗證 (OAuth 2.0)             │
│ 4. 權限控制 (RBAC)                  │
│ 5. 稽核日誌 (完整記錄)              │
│ 6. 資料遮罩 (敏感資訊)              │
└─────────────────────────────────────┘
```

---

## 📦 部署架構

```
                    ┌─────────────┐
                    │  Azure LB   │  負載平衡
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐    ┌─────▼─────┐    ┌────▼──────┐
    │  Django   │    │  Django   │    │  Django   │
    │  Web App  │    │  Web App  │    │  Web App  │
    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
          │                │                 │
          └────────────────┼─────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
          ┌─────▼─────┐         ┌────▼──────┐
          │   Redis   │         │ PostgreSQL│
          │  (Cache)  │         │    (DB)   │
          └───────────┘         └───────────┘
                │
          ┌─────▼─────┐
          │  Celery   │  異步任務
          │  Workers  │
          └───────────┘
                │
          ┌─────▼─────────────────┐
          │   Azure Services      │
          │  • Document Intel.    │
          │  • OpenAI GPT         │
          │  • Blob Storage       │
          └───────────────────────┘
```

---

## 🎓 學習資源與參考

### Azure 服務文件
- [Azure Document Intelligence](https://learn.microsoft.com/azure/ai-services/document-intelligence/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)

### 相關技術
- Django Best Practices
- Celery Async Tasks
- GPT Prompt Engineering

---

## 📞 快速聯絡

**專案**：台北智慧城市估驗計價自動化系統  
**技術棧**：Azure DI + GPT-4 + Django + AI Rules Engine  
**狀態**：架構設計階段

---

*此文件為技術概覽速查表，詳細架構請參考 PROJECT_ARCHITECTURE.md*
