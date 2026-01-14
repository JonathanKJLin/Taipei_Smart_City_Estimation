"""
估驗計價相關的 JSON Schema 定義

TODO: 待有實際文件範本後完善 Schema 細節
"""


# 估驗計價單 Schema
ESTIMATION_PAYMENT_SCHEMA = {
  "type": "object",
  "properties": {
    "document_type": { 
      "type": "string", 
      "description": "文件類型",
      "enum": ["估驗計價單"]
    },
    "document_id": { 
      "type": "string", 
      "description": "文件唯一識別碼" 
    },
    "document_info": {
      "type": "object",
      "properties": {
        "agency_name": { "type": "string", "description": "機關名稱" },
        "period_number": { "type": "integer", "description": "估驗次別(A8)" },
        "estimation_period": { "type": "string", "description": "估驗期間(A7)" }
      }
    },
    "contract_financials": {
      "type": "object",
      "properties": {
        "original_amount": { "type": "number", "description": "原契約金額(A9)" },
        "current_total_amount": { "type": "number", "description": "變更後契約金額(A10)" },
        "prepayment_total": { "type": "number", "description": "累計撥付預付款(A11)" }
      }
    },
    "current_period_data": {
      "type": "object",
      "description": "原始提取數據 (Raw Data)",
      "properties": {
        "C": { "type": "number", "description": "本次估驗計價款" },
        "D": { "type": "number", "description": "物價指數調整款" },
        "E": { "type": "number", "description": "扣款" },
        "F": { "type": "number", "description": "保留款" },
        "G": { "type": "number", "description": "扣回預付款" },
        "H": { "type": "number", "description": "應付金額" },
        "K": { "type": "number", "description": "實付金額" }
      }
    },
    "logic_config": {
      "type": "object",
      "description": "動態公式定義區",
      "properties": {
        "formulas": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "target_field": { "type": "string", "description": "目標欄位代號(如H)" },
              "expression": { "type": "string", "description": "計算表達式，例如：'C + D - E - F - G'" },
              "rounding_rule": { "type": "string", "enum": ["round", "floor", "ceil"], "description": "進捨位方式 " }
            },
            "required": ["target_field", "expression"]
          }
        },
        "thresholds": {
          "type": "object",
          "description": "參數閾值，例如預付款扣回區間(20%-80%)"
        }
      }
    },
    "validation_log": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "field": { "type": "string" },
          "extracted_value": { "type": "number" },
          "calculated_value": { "type": "number" },
          "is_match": { "type": "boolean" },
          "delta": { "type": "number" }
        },
        "required": ["field", "is_match"]
      }
    },
    "confidence_scores": {
      "type": "object",
      "description": "各階段信心分數",
      "$ref": "#/definitions/confidence_score"
    },
    "metadata": {
      "type": "object",
      "description": "元資料",
      "properties": {
        "processed_timestamp": { "type": "string", "format": "date-time" },
        "system_version": { "type": "string" },
        "processor": { "type": "string" }
      }
    }
  },
  "required": ["document_type", "document_id", "document_info", "current_period_data"],
  "definitions": {
    "confidence_score": {
      "type": "object",
      "properties": {
        "overall": { "type": "number", "minimum": 0, "maximum": 1 },
        "icr_accuracy": { "type": "number", "minimum": 0, "maximum": 1 },
        "field_mapping": { "type": "number", "minimum": 0, "maximum": 1 },
        "logic_understanding": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}


# 合約資訊 Schema
CONTRACT_INFO_SCHEMA = {
    "type": "object",
    "properties": {
        "contract_number": { "type": "string", "description": "合約編號" },
        "contract_name": { "type": "string", "description": "合約名稱" },
        "contractor": { "type": "string", "description": "承包商" },
        "owner": { "type": "string", "description": "業主單位" },
        "start_date": { "type": "string", "format": "date", "description": "開工日期" },
        "end_date": { "type": "string", "format": "date", "description": "完工日期" },
        "original_amount": { "type": "number", "description": "原契約金額" },
        "current_amount": { "type": "number", "description": "變更後契約金額" }
    },
    "required": ["contract_number", "contract_name"]
}


# 驗算結果 Schema
VALIDATION_RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "amount_validation": {
            "type": "object",
            "description": "金額驗算結果",
            "properties": {
                "vertical_sum": {"$ref": "#/definitions/check_result"},
                "horizontal_calc": {"$ref": "#/definitions/check_result"},
                "subtotal_check": {"$ref": "#/definitions/check_result"}
            }
        },
        "accumulation_validation": {
            "type": "object",
            "description": "累計檢核結果",
            "properties": {
                "logic_check": {"$ref": "#/definitions/check_result"},
                "contract_limit": {"$ref": "#/definitions/check_result"},
                "progress_check": {"$ref": "#/definitions/check_result"}
            }
        },
        "payment_condition_validation": {
            "type": "object",
            "description": "付款條件驗證結果",
            "properties": {
                "condition_check": {"$ref": "#/definitions/check_result"}
            }
        }
    },
    "definitions": {
        "check_result": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pass", "fail", "warning", "error"]
                },
                "message": {"type": "string"},
                "details": {"type": "object"}
            }
        }
    }
}


# 信心分數 Schema
CONFIDENCE_SCORE_SCHEMA = {
    "type": "object",
    "properties": {
        "overall": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "整體信心分數"
        },
        "icr_accuracy": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "ICR 準確度"
        },
        "field_mapping": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "欄位對應準確度"
        },
        "logic_understanding": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "邏輯理解準確度"
        },
        "validation_confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "驗算信心度"
        }
    }
}


def get_schema_by_document_type(doc_type: str) -> dict:
    """
    根據文件類型取得對應的 Schema
    
    Args:
        doc_type: 文件類型
    
    Returns:
        dict: 對應的 JSON Schema
    """
    schemas = {
        "估驗計價單": ESTIMATION_PAYMENT_SCHEMA,
        "合約資訊": CONTRACT_INFO_SCHEMA,
        "驗算結果": VALIDATION_RESULT_SCHEMA,
        "信心分數": CONFIDENCE_SCORE_SCHEMA
    }
    
    return schemas.get(doc_type, ESTIMATION_PAYMENT_SCHEMA)
