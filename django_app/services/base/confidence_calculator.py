"""
Confidence Score Calculator
計算各種處理結果的信心分數

從 AZTL 專案重用
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ConfidenceCalculator:
    """信心分數計算器"""
    
    @staticmethod
    def calculate_icr_confidence(icr_result: Dict[str, Any]) -> float:
        """
        計算 ICR 結果的信心分數
        
        Args:
            icr_result: ICR 結果資料
        
        Returns:
            float: 信心分數 (0-1)
        """
        try:
            # TODO: 根據實際 ICR 結果結構實作
            # 目前返回預設值
            
            confidence_scores = []
            
            # 從各個元素提取信心分數
            if "pages" in icr_result:
                for page in icr_result["pages"]:
                    if "confidence" in page:
                        confidence_scores.append(page["confidence"])
            
            # 計算平均值
            if confidence_scores:
                return sum(confidence_scores) / len(confidence_scores)
            
            return 0.8  # 預設值
            
        except Exception as e:
            logger.error(f"Error calculating ICR confidence: {e}")
            return 0.0
    
    @staticmethod
    def calculate_field_mapping_confidence(
        mapped_data: Dict[str, Any],
        required_fields: List[str]
    ) -> float:
        """
        計算欄位對應的信心分數
        
        Args:
            mapped_data: 對應後的資料
            required_fields: 必要欄位列表
        
        Returns:
            float: 信心分數 (0-1)
        """
        try:
            if not required_fields:
                return 1.0
            
            # 檢查必要欄位是否都有對應
            found_count = 0
            for field in required_fields:
                if field in mapped_data and mapped_data[field]:
                    found_count += 1
            
            base_confidence = found_count / len(required_fields)
            
            # 考慮欄位值的品質
            quality_scores = []
            for field, value in mapped_data.items():
                if value is None or value == "":
                    quality_scores.append(0.0)
                elif isinstance(value, str) and len(value) < 2:
                    quality_scores.append(0.5)
                else:
                    quality_scores.append(1.0)
            
            quality_confidence = sum(quality_scores) / len(quality_scores) if quality_scores else 1.0
            
            # 綜合計算
            final_confidence = (base_confidence * 0.7) + (quality_confidence * 0.3)
            
            return final_confidence
            
        except Exception as e:
            logger.error(f"Error calculating field mapping confidence: {e}")
            return 0.0
    
    @staticmethod
    def calculate_validation_confidence(
        validation_results: Dict[str, Any]
    ) -> float:
        """
        計算驗證結果的信心分數
        
        Args:
            validation_results: 驗證結果
        
        Returns:
            float: 信心分數 (0-1)
        """
        try:
            pass_count = 0
            total_count = 0
            
            # 統計通過的驗證項目
            for category, checks in validation_results.items():
                if isinstance(checks, dict):
                    for check_name, result in checks.items():
                        total_count += 1
                        if isinstance(result, dict) and result.get("status") == "pass":
                            pass_count += 1
            
            if total_count == 0:
                return 1.0
            
            return pass_count / total_count
            
        except Exception as e:
            logger.error(f"Error calculating validation confidence: {e}")
            return 0.0
    
    @staticmethod
    def calculate_overall_confidence(
        icr_confidence: float,
        mapping_confidence: float,
        validation_confidence: float,
        weights: Dict[str, float] = None
    ) -> float:
        """
        計算整體信心分數
        
        Args:
            icr_confidence: ICR 信心分數
            mapping_confidence: 欄位對應信心分數
            validation_confidence: 驗證信心分數
            weights: 各項權重 (預設: ICR=0.3, Mapping=0.4, Validation=0.3)
        
        Returns:
            float: 整體信心分數 (0-1)
        """
        try:
            if weights is None:
                weights = {
                    "icr": 0.3,
                    "mapping": 0.4,
                    "validation": 0.3
                }
            
            overall = (
                icr_confidence * weights.get("icr", 0.3) +
                mapping_confidence * weights.get("mapping", 0.4) +
                validation_confidence * weights.get("validation", 0.3)
            )
            
            return min(max(overall, 0.0), 1.0)  # 確保在 0-1 範圍內
            
        except Exception as e:
            logger.error(f"Error calculating overall confidence: {e}")
            return 0.0
