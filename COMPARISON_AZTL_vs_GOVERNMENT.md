# 專案對比：AZTL 保險核保系統 vs 政府估驗計價系統

## 📊 專案概覽對比

| 維度 | AZTL 保險核保專案 | 政府估驗計價專案 |
|------|------------------|-----------------|
| **客戶** | AZTL 保險公司 | 台北市政府單位 |
| **領域** | 保險業 (Insurance Underwriting) | 政府工程管理 |
| **文件類型** | 要保書、健康告知書、批註條款等 | 估驗計價單、付款明細、工程合約 |
| **核心目標** | 自動化保險核保流程 | 自動化工程驗算與付款檢核 |
| **驗證邏輯** | 保單資料完整性、適合度評估 | 金額加總、累計檢核、付款條件 |

---

## 🔄 可重用的核心架構

### ✅ 保留的核心技術與架構

```
┌─────────────────────────────────────────────────────────┐
│                  可直接重用的部分                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Django 應用框架結構                                  │
│     ✓ settings 分層設計 (dev/prod)                      │
│     ✓ apps 模組化架構                                    │
│     ✓ services 服務層設計                                │
│                                                          │
│  2. Azure Document Intelligence 整合                    │
│     ✓ azure_service.py (ICR 智能字元識別與文件掃描)      │
│     ✓ pdf_splitter.py (PDF 處理)                        │
│     ✓ file_handlers.py (檔案處理工具)                    │
│                                                          │
│  3. Azure OpenAI GPT 整合                               │
│     ✓ azure_gpt_page_processor.py (GPT 處理邏輯)       │
│     ✓ Prompt Engineering 架構                            │
│     ✓ Few-shot Learning 機制                            │
│                                                          │
│  4. 資料處理流程                                         │
│     ✓ 文件上傳機制                                       │
│     ✓ 異步任務處理 (Celery)                              │
│     ✓ JSON Schema 標準化輸出                            │
│                                                          │
│  5. 驗證與信心分數機制                                   │
│     ✓ confidence_calculator.py                          │
│     ✓ validation_service.py 基礎架構                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 🔧 需要調整的部分

```
┌─────────────────────────────────────────────────────────┐
│              需要客製化調整的部分                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. JSON Schema 定義                                    │
│     ✗ insurance_schema_v1.py                            │
│     ✓ 新建：estimation_payment_schema.py                │
│                                                          │
│  2. Prompt Templates                                    │
│     ✗ services/templates/prompt/*.txt (保險相關)        │
│     ✓ 新建：估驗計價相關 prompts                         │
│                                                          │
│  3. JSON Format Templates                               │
│     ✗ services/templates/json_format/*.json (保單)     │
│     ✓ 新建：估驗計價 JSON templates                     │
│                                                          │
│  4. 驗證邏輯規則                                         │
│     ✗ key_validation_service.py (保險欄位驗證)          │
│     ✓ 新建：estimation_validation_service.py            │
│            (金額、累計、付款條件驗證)                     │
│                                                          │
│  5. 業務邏輯服務                                         │
│     ✗ ai_doc_service.py (保險文件處理)                  │
│     ✓ 調整為：estimation_doc_service.py                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 🆕 需要新增的核心模組

```
┌─────────────────────────────────────────────────────────┐
│                新增的專屬模組                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. 金額驗算引擎                                         │
│     ✓ amount_calculation_engine.py                      │
│        - 直式加總檢核                                     │
│        - 橫式加總檢核                                     │
│        - 小計/總計驗算                                    │
│                                                          │
│  2. 累計檢核模組                                         │
│     ✓ accumulation_checker.py                           │
│        - 前期累計 + 本期 = 本期累計                       │
│        - 歷史資料追蹤                                     │
│        - 合約總額上限管控                                 │
│                                                          │
│  3. 付款條件引擎                                         │
│     ✓ payment_condition_engine.py                       │
│        - 條件解析 (NLP)                                  │
│        - 進度比對                                         │
│        - 付款比例驗算                                     │
│                                                          │
│  4. 規則學習模組                                         │
│     ✓ rules_learning_module.py                          │
│        - 規則自動萃取                                     │
│        - 規則庫管理                                       │
│        - 動態規則更新                                     │
│                                                          │
│  5. 回饋機制                                             │
│     ✓ feedback_loop_service.py                          │
│        - HITL (Human-in-the-loop)                       │
│        - 錯誤案例收集                                     │
│        - 模型持續優化                                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 建議的專案目錄結構調整

### 原 AZTL 專案結構
```
django_app/
├── apps/
│   └── ai_driven_document_processor/  # 保險文件處理
├── services/
│   ├── azure_service.py               # ✓ 可重用
│   ├── azure_gpt_page_processor.py    # ✓ 可重用
│   ├── ai_doc_service.py              # ✗ 需調整
│   ├── key_validation_service.py      # ✗ 需調整
│   └── templates/
│       ├── json_format/               # ✗ 保險相關
│       └── prompt/                    # ✗ 保險相關
└── schemas/
    └── insurance_schema_v1.py         # ✗ 保險 Schema
```

### 建議的新專案結構
```
django_app/
├── apps/
│   ├── document_processor/            # 通用文件處理 (重用)
│   └── estimation_validator/          # 新增：估驗計價驗證
├── services/
│   ├── base/                          # 基礎服務 (重用)
│   │   ├── azure_service.py
│   │   ├── azure_gpt_processor.py
│   │   ├── pdf_handler.py
│   │   └── confidence_calculator.py
│   ├── estimation/                    # 新增：估驗計價專屬
│   │   ├── amount_engine.py           # 金額驗算引擎
│   │   ├── accumulation_checker.py    # 累計檢核
│   │   ├── payment_condition_engine.py # 付款條件引擎
│   │   └── rules_learning.py          # 規則學習
│   ├── validation/                    # 驗證服務
│   │   └── estimation_validator.py    # 估驗計價驗證邏輯
│   └── templates/
│       ├── json_format/
│       │   ├── estimation_payment.json      # 估驗計價單
│       │   ├── payment_detail.json          # 付款明細
│       │   └── contract_info.json           # 合約資訊
│       └── prompt/
│           ├── estimation_extraction.txt    # 資料擷取
│           ├── logic_recognition.txt        # 邏輯識別
│           └── payment_condition_parse.txt  # 付款條件解析
├── schemas/
│   ├── common.py                      # ✓ 可重用
│   └── estimation_schema_v1.py        # 新增：估驗計價 Schema
└── utils/
    ├── file_handlers.py               # ✓ 可重用
    └── storage.py                     # ✓ 可重用
```

---

## 🎯 核心差異：驗證邏輯對比

### AZTL 保險核保系統
```python
# 驗證重點：資料完整性與合規性
validation_rules = {
    "completeness": [
        "投保人基本資料完整性",
        "受益人資料完整性",
        "健康告知事項完整性"
    ],
    "consistency": [
        "年齡與生日一致性",
        "保額與收入合理性",
        "批註條款一致性"
    ],
    "compliance": [
        "適合度評估符合性",
        "高齡投保評估",
        "AML/KYC 檢核"
    ]
}
```

### 政府估驗計價系統
```python
# 驗證重點：金額計算與邏輯正確性
validation_rules = {
    "amount_calculation": [
        "直式加總正確性",
        "橫式加總正確性",
        "小計與總計驗算"
    ],
    "accumulation": [
        "前期累計 + 本期 = 本期累計",
        "累計金額不超過合約總額",
        "各期金額合理性"
    ],
    "payment_condition": [
        "付款條件符合性",
        "進度與付款比例一致性",
        "付款金額計算正確性"
    ],
    "rules_engine": [
        "自定義規則驗證",
        "條件邏輯檢核",
        "異常偵測與標記"
    ]
}
```

---

## 🚀 遷移策略建議

### 階段一：環境建置與基礎架構遷移 (Week 1-2)
1. 複製 AZTL 專案作為基礎
2. 保留所有 Azure 整合相關程式碼
3. 重構目錄結構 (上述建議結構)
4. 移除保險相關的 templates 與 schemas

### 階段二：客製化開發 (Week 3-6)
1. 開發估驗計價 JSON Schema
2. 撰寫估驗計價相關 Prompts
3. 開發三大核心引擎：
   - 金額驗算引擎
   - 累計檢核模組
   - 付款條件引擎

### 階段三：規則學習與優化 (Week 7-8)
1. 實作規則學習模組
2. 建立回饋機制
3. 模型訓練與調優

### 階段四：測試與部署 (Week 9-10)
1. 單元測試與整合測試
2. 使用實際文件驗證
3. 效能優化與部署

---

## 💡 關鍵技術挑戰對比

| 技術挑戰 | AZTL 專案 | 政府專案 | 難度 |
|---------|----------|----------|------|
| **文件結構複雜度** | 中等 (表單類) | 高 (表格+條件敘述) | ⬆️ |
| **邏輯驗算** | 低 (主要是資料完整性) | 高 (需計算驗證) | ⬆️⬆️ |
| **NLP 理解需求** | 中等 (欄位對應) | 高 (邏輯關聯、條件解析) | ⬆️ |
| **規則動態性** | 低 (保險規則固定) | 高 (需自動學習規則) | ⬆️⬆️ |
| **回饋學習** | 無 | 必須 | 🆕 |

---

## 📋 總結

### ✅ 可重用的優勢
- 成熟的 Django 架構
- 已驗證的 Azure DI + GPT 整合
- 完整的文件處理流程
- 標準化輸出機制

### 🎯 需要強化的部分
- **計算驗證能力**：金額加總、累計檢核
- **邏輯理解能力**：付款條件、規則識別
- **自動學習機制**：規則引擎動態優化
- **回饋循環**：HITL 機制建立

### 💪 技術挑戰
估驗計價專案在**邏輯驗算**與**規則學習**方面的需求更高，需要更強大的 AI 能力與更精密的驗證引擎，但基礎架構可以大量重用 AZTL 專案的成果。

---

*建議：在現有 AZTL 專案基礎上進行客製化開發，可節省 40-50% 的基礎建設時間。*
