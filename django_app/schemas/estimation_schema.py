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
            "enum": ["估驗計價單", "付款明細", "工程合約", "其他"]
        },
        "document_id": {
            "type": "string",
            "description": "文件編號"
        },
        "period_number": {
            "type": "integer",
            "description": "期數"
        },
        "contract_info": {
            "type": "object",
            "properties": {
                "contract_number": {"type": "string"},
                "contract_name": {"type": "string"},
                "contract_amount": {"type": "number"},
                "contractor": {"type": "string"},
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"}
            }
        },
        "items": {
            "type": "array",
            "description": "項目明細",
            "items": {
                "type": "object",
                "properties": {
                    "item_no": {"type": "string"},
                    "description": {"type": "string"},
                    "unit": {"type": "string"},
                    "quantity": {"type": "number"},
                    "unit_price": {"type": "number"},
                    "amount": {"type": "number"},
                    "previous_quantity": {"type": "number"},
                    "total_quantity": {"type": "number"},
                    "remarks": {"type": "string"}
                }
            }
        },
        "period_amount": {
            "type": "number",
            "description": "本期金額"
        },
        "previous_accumulation": {
            "type": "number",
            "description": "前期累計"
        },
        "current_accumulation": {
            "type": "number",
            "description": "本期累計"
        },
        "payment_conditions": {
            "type": "array",
            "description": "付款條件",
            "items": {
                "type": "object",
                "properties": {
                    "condition_text": {"type": "string"},
                    "parsed_condition": {"type": "object"}
                }
            }
        },
        "validation_results": {
            "type": "object",
            "description": "驗算結果"
        },
        "confidence_scores": {
            "type": "object",
            "description": "信心分數"
        },
        "metadata": {
            "type": "object",
            "description": "元資料"
        }
    },
    "required": ["document_type", "document_id"]
}


# 合約資訊 Schema
CONTRACT_INFO_SCHEMA = {
    "type": "object",
    "properties": {
        "contract_number": {
            "type": "string",
            "description": "合約編號"
        },
        "contract_name": {
            "type": "string",
            "description": "合約名稱"
        },
        "contract_amount": {
            "type": "number",
            "description": "合約總金額"
        },
        "contractor": {
            "type": "string",
            "description": "承包商"
        },
        "owner": {
            "type": "string",
            "description": "業主單位"
        },
        "start_date": {
            "type": "string",
            "format": "date",
            "description": "開工日期"
        },
        "end_date": {
            "type": "string",
            "format": "date",
            "description": "完工日期"
        },
        "payment_terms": {
            "type": "string",
            "description": "付款條件說明"
        }
    }
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
