"""
Schema Validator
JSON Schema 驗證器

驗證資料是否符合定義的 Schema
"""
import logging
from typing import Dict, Any, List, Tuple
import json

logger = logging.getLogger(__name__)


class SchemaValidator:
    """
    JSON Schema 驗證器
    確保資料符合預定義的結構
    """
    
    def validate(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        驗證資料是否符合 Schema
        
        Args:
            data: 待驗證的資料
            schema: JSON Schema
        
        Returns:
            Tuple[bool, List[str]]: (是否通過, 錯誤訊息列表)
        """
        logger.info("Validating data against schema")
        
        errors = []
        
        try:
            # 驗證必要欄位
            if "required" in schema:
                for field in schema["required"]:
                    if field not in data:
                        errors.append(f"缺少必要欄位: {field}")
            
            # 驗證欄位型別
            if "properties" in schema:
                for field, field_schema in schema["properties"].items():
                    if field in data:
                        field_errors = self._validate_field(
                            field, data[field], field_schema
                        )
                        errors.extend(field_errors)
            
            # 驗證enum值
            self._validate_enums(data, schema, errors)
            
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("Schema validation passed")
            else:
                logger.warning(f"Schema validation failed with {len(errors)} errors")
            
            return is_valid, errors
            
        except Exception as e:
            logger.error(f"Error during schema validation: {e}")
            return False, [f"驗證過程發生錯誤: {str(e)}"]
    
    def _validate_field(
        self,
        field_name: str,
        value: Any,
        field_schema: Dict[str, Any]
    ) -> List[str]:
        """
        驗證單一欄位
        
        Args:
            field_name: 欄位名稱
            value: 欄位值
            field_schema: 欄位 Schema
        
        Returns:
            List[str]: 錯誤訊息列表
        """
        errors = []
        
        # 驗證型別
        if "type" in field_schema:
            expected_type = field_schema["type"]
            if not self._check_type(value, expected_type):
                errors.append(
                    f"欄位 '{field_name}' 型別錯誤: "
                    f"期望 {expected_type}, 實際 {type(value).__name__}"
                )
        
        # 驗證數值範圍
        if isinstance(value, (int, float)):
            if "minimum" in field_schema and value < field_schema["minimum"]:
                errors.append(
                    f"欄位 '{field_name}' 小於最小值 {field_schema['minimum']}"
                )
            if "maximum" in field_schema and value > field_schema["maximum"]:
                errors.append(
                    f"欄位 '{field_name}' 大於最大值 {field_schema['maximum']}"
                )
        
        # 驗證陣列
        if isinstance(value, list) and "items" in field_schema:
            for idx, item in enumerate(value):
                item_errors = self._validate_field(
                    f"{field_name}[{idx}]",
                    item,
                    field_schema["items"]
                )
                errors.extend(item_errors)
        
        # 驗證物件
        if isinstance(value, dict) and "properties" in field_schema:
            for prop_name, prop_schema in field_schema["properties"].items():
                if prop_name in value:
                    prop_errors = self._validate_field(
                        f"{field_name}.{prop_name}",
                        value[prop_name],
                        prop_schema
                    )
                    errors.extend(prop_errors)
        
        return errors
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """
        檢查值的型別
        
        Args:
            value: 值
            expected_type: 期望的型別
        
        Returns:
            bool: 是否符合型別
        """
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None)
        }
        
        expected_python_type = type_mapping.get(expected_type)
        
        if expected_python_type is None:
            return True  # 未知型別，不驗證
        
        return isinstance(value, expected_python_type)
    
    def _validate_enums(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any],
        errors: List[str]
    ):
        """
        驗證 enum 值
        
        Args:
            data: 資料
            schema: Schema
            errors: 錯誤列表（會被修改）
        """
        if "properties" not in schema:
            return
        
        for field, field_schema in schema["properties"].items():
            if field in data and "enum" in field_schema:
                value = data[field]
                allowed_values = field_schema["enum"]
                if value not in allowed_values:
                    errors.append(
                        f"欄位 '{field}' 的值 '{value}' 不在允許的值列表中: {allowed_values}"
                    )
    
    def validate_document_structure(
        self,
        data: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        驗證文件基本結構
        
        Args:
            data: 文件資料
        
        Returns:
            Tuple[bool, List[str]]: (是否通過, 錯誤訊息列表)
        """
        errors = []
        
        # 基本必要欄位
        required_fields = ["document_type", "document_id"]
        for field in required_fields:
            if field not in data:
                errors.append(f"缺少基本欄位: {field}")
        
        # 檢查資料是否為空
        if not data:
            errors.append("文件資料為空")
        
        return len(errors) == 0, errors
    
    def get_schema_for_document_type(
        self,
        document_type: str
    ) -> Dict[str, Any]:
        """
        根據文件類型取得對應的 Schema
        
        Args:
            document_type: 文件類型
        
        Returns:
            Dict: JSON Schema
        """
        # TODO: 從 schemas 模組載入對應的 Schema
        from django_app.schemas.estimation_schema import get_schema_by_document_type
        
        try:
            return get_schema_by_document_type(document_type)
        except Exception as e:
            logger.error(f"Error loading schema for {document_type}: {e}")
            return {}


# 單例模式
_schema_validator = None

def get_schema_validator() -> SchemaValidator:
    """取得 Schema 驗證器實例"""
    global _schema_validator
    if _schema_validator is None:
        _schema_validator = SchemaValidator()
    return _schema_validator
