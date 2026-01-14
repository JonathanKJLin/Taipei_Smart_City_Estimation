"""
付款條件驗算引擎
處理付款條件的解析與驗證

TODO: 待有實際文件範本後實作具體解析與驗算規則
"""
import logging
import re
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class PaymentConditionEngine:
    """
    付款條件驗算引擎
    負責解析付款條件並驗證其符合性
    """
    
    def parse_condition(
        self,
        condition_text: str,
        use_gpt: bool = True
    ) -> Dict[str, Any]:
        """
        解析付款條件文字描述
        
        Args:
            condition_text: 付款條件文字
            use_gpt: 是否使用 GPT 進行解析
        
        Returns:
            Dict: 結構化的付款條件
        """
        # TODO: 實作具體解析邏輯
        # 方案1: 使用 GPT-5 進行自然語言解析
        # 方案2: 使用正則表達式 + 規則引擎
        
        logger.info(f"Parsing payment condition: {condition_text}")
        
        if use_gpt:
            return self._parse_with_gpt(condition_text)
        else:
            return self._parse_with_rules(condition_text)
    
    def _parse_with_gpt(self, condition_text: str) -> Dict[str, Any]:
        """
        使用 GPT 解析付款條件
        
        Args:
            condition_text: 付款條件文字
        
        Returns:
            Dict: 結構化的付款條件
        """
        # TODO: 整合 GPT 服務
        from ..base.azure_gpt_service import get_azure_gpt_service
        
        try:
            gpt_service = get_azure_gpt_service()
            result = gpt_service.parse_payment_conditions(condition_text)
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing with GPT: {e}")
            return {
                "error": str(e),
                "original_text": condition_text
            }
    
    def _parse_with_rules(self, condition_text: str) -> Dict[str, Any]:
        """
        使用規則引擎解析付款條件
        
        Args:
            condition_text: 付款條件文字
        
        Returns:
            Dict: 結構化的付款條件
        """
        # TODO: 實作規則引擎
        # 例如：
        # - "工程完成30%後支付第二期款" -> {"trigger": "progress", "threshold": 30, "payment_phase": 2}
        # - "驗收合格後支付尾款" -> {"trigger": "acceptance", "payment_type": "final"}
        
        logger.info(f"Parsing with rules: {condition_text}")
        
        parsed_condition = {
            "original_text": condition_text,
            "trigger_type": None,  # progress, time, milestone, acceptance
            "threshold": None,
            "payment_phase": None,
            "payment_percentage": None,
            "conditions": []
        }
        
        # 示例規則（需根據實際情況擴充）
        # 進度條件
        progress_pattern = r'工程完成.*?(\d+(?:\.\d+)?)%.*?(?:第([一二三四五\d]+)期|第(\d+)期)'
        match = re.search(progress_pattern, condition_text)
        if match:
            parsed_condition["trigger_type"] = "progress"
            parsed_condition["threshold"] = float(match.group(1))
            parsed_condition["payment_phase"] = self._convert_chinese_number(match.group(2)) if match.group(2) else int(match.group(3))
        
        # 驗收條件
        if "驗收" in condition_text:
            parsed_condition["trigger_type"] = "acceptance"
            if "合格" in condition_text:
                parsed_condition["conditions"].append("acceptance_passed")
        
        # 時間條件
        time_pattern = r'(\d+)個?月'
        match = re.search(time_pattern, condition_text)
        if match:
            parsed_condition["trigger_type"] = "time"
            parsed_condition["threshold"] = int(match.group(1))
        
        return parsed_condition
    
    def validate_payment(
        self,
        parsed_condition: Dict[str, Any],
        actual_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        驗證付款是否符合條件
        
        Args:
            parsed_condition: 解析後的付款條件
            actual_data: 實際資料（進度、狀態等）
        
        Returns:
            Dict: 驗證結果
        """
        # TODO: 實作具體驗證邏輯
        
        logger.info("Validating payment condition")
        
        try:
            trigger_type = parsed_condition.get("trigger_type")
            
            if trigger_type == "progress":
                return self._validate_progress_condition(parsed_condition, actual_data)
            elif trigger_type == "acceptance":
                return self._validate_acceptance_condition(parsed_condition, actual_data)
            elif trigger_type == "time":
                return self._validate_time_condition(parsed_condition, actual_data)
            elif trigger_type == "milestone":
                return self._validate_milestone_condition(parsed_condition, actual_data)
            else:
                return {
                    "status": "warning",
                    "message": "無法識別的付款條件類型"
                }
        
        except Exception as e:
            logger.error(f"Error validating payment: {e}")
            return {
                "status": "error",
                "message": f"驗證過程發生錯誤：{str(e)}"
            }
    
    def _validate_progress_condition(
        self,
        condition: Dict[str, Any],
        actual_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """驗證進度條件"""
        # TODO: 實作具體邏輯
        
        required_progress = condition.get("threshold", 0)
        actual_progress = actual_data.get("progress_percentage", 0)
        
        if actual_progress >= required_progress:
            return {
                "status": "pass",
                "message": f"實際進度 {actual_progress}% 已達到要求 {required_progress}%",
                "required_progress": required_progress,
                "actual_progress": actual_progress
            }
        else:
            return {
                "status": "fail",
                "message": f"實際進度 {actual_progress}% 未達要求 {required_progress}%",
                "required_progress": required_progress,
                "actual_progress": actual_progress
            }
    
    def _validate_acceptance_condition(
        self,
        condition: Dict[str, Any],
        actual_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """驗證驗收條件"""
        # TODO: 實作具體邏輯
        return {"status": "pass", "message": "驗收條件驗證功能待實作"}
    
    def _validate_time_condition(
        self,
        condition: Dict[str, Any],
        actual_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """驗證時間條件"""
        # TODO: 實作具體邏輯
        return {"status": "pass", "message": "時間條件驗證功能待實作"}
    
    def _validate_milestone_condition(
        self,
        condition: Dict[str, Any],
        actual_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """驗證里程碑條件"""
        # TODO: 實作具體邏輯
        return {"status": "pass", "message": "里程碑條件驗證功能待實作"}
    
    @staticmethod
    def _convert_chinese_number(chinese_num: str) -> int:
        """轉換中文數字為阿拉伯數字"""
        chinese_to_arabic = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }
        
        return chinese_to_arabic.get(chinese_num, 0)
    
    def extract_conditions_from_document(
        self,
        document_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        從文件中提取所有付款條件
        
        Args:
            document_data: 文件資料
        
        Returns:
            List[Dict]: 提取的付款條件列表
        """
        # TODO: 實作條件提取邏輯
        
        logger.info("Extracting payment conditions from document")
        
        conditions = []
        
        # 從合約資訊中提取（兼容新舊 Schema）
        contract_info = (
            document_data.get("contract_financials") or 
            document_data.get("contract_info", {})
        )
        payment_terms = contract_info.get("payment_terms", "")
        
        if payment_terms:
            parsed = self.parse_condition(payment_terms)
            conditions.append(parsed)
        
        # 如果文件中已有解析好的付款條件（新 Schema）
        if "payment_conditions" in document_data:
            for condition in document_data["payment_conditions"]:
                conditions.append(condition)
        
        return conditions


# 單例模式
_payment_engine = None

def get_payment_engine() -> PaymentConditionEngine:
    """取得付款條件引擎實例"""
    global _payment_engine
    if _payment_engine is None:
        _payment_engine = PaymentConditionEngine()
    return _payment_engine
