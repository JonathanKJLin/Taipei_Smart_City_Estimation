"""
金額驗算引擎
處理金額加總、橫式計算等驗算邏輯

TODO: 待有實際文件範本後實作具體運算規則
"""
import logging
from typing import Dict, Any, List
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)


class AmountCalculationEngine:
    """
    金額驗算引擎
    負責驗證各種金額計算邏輯
    """
    
    def validate_all(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        執行所有金額驗算
        
        Args:
            data: 標準化的估驗計價資料
        
        Returns:
            Dict: 驗算結果
        """
        results = {
            "vertical_sum": self.validate_vertical_sum(data),
            "horizontal_calculation": self.validate_horizontal_calculation(data),
            "subtotal_check": self.validate_subtotal(data),
            "total_check": self.validate_total(data)
        }
        
        # 判斷整體是否通過
        all_passed = all(
            result.get("status") == "pass" 
            for result in results.values()
        )
        
        results["overall_status"] = "pass" if all_passed else "fail"
        
        return results
    
    def validate_vertical_sum(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        驗證直式加總 (欄位內的數值加總)
        例如：所有項目的金額加總應等於總金額
        
        Args:
            data: 估驗計價資料
        
        Returns:
            Dict: 驗算結果
        """
        # TODO: 實作具體邏輯
        # 需要根據實際文件範本確定：
        # 1. 哪些欄位需要加總
        # 2. 加總結果應該與哪個欄位比對
        # 3. 允許的誤差範圍
        
        logger.info("Executing vertical sum validation")
        
        try:
            # 框架邏輯示例
            items = data.get("items", [])
            declared_total = data.get("total_amount", 0)
            
            # 計算實際加總
            calculated_total = Decimal(0)
            for item in items:
                amount = item.get("amount", 0)
                calculated_total += Decimal(str(amount))
            
            # 比對
            difference = abs(calculated_total - Decimal(str(declared_total)))
            tolerance = Decimal("0.01")  # 允許的誤差
            
            if difference <= tolerance:
                return {
                    "status": "pass",
                    "message": "直式加總驗證通過",
                    "calculated": float(calculated_total),
                    "declared": declared_total,
                    "difference": float(difference)
                }
            else:
                return {
                    "status": "fail",
                    "message": f"直式加總不符：差異 {difference}",
                    "calculated": float(calculated_total),
                    "declared": declared_total,
                    "difference": float(difference)
                }
            
        except (ValueError, InvalidOperation, TypeError) as e:
            logger.error(f"Error in vertical sum validation: {e}")
            return {
                "status": "error",
                "message": f"驗證過程發生錯誤：{str(e)}"
            }
    
    def validate_horizontal_calculation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        驗證橫式計算 (同一行內的計算邏輯)
        例如：單價 × 數量 = 金額
        
        Args:
            data: 估驗計價資料
        
        Returns:
            Dict: 驗算結果
        """
        # TODO: 實作具體邏輯
        
        logger.info("Executing horizontal calculation validation")
        
        try:
            items = data.get("items", [])
            failed_items = []
            
            for idx, item in enumerate(items):
                # 框架邏輯示例
                unit_price = Decimal(str(item.get("unit_price", 0)))
                quantity = Decimal(str(item.get("quantity", 0)))
                declared_amount = Decimal(str(item.get("amount", 0)))
                
                calculated_amount = unit_price * quantity
                difference = abs(calculated_amount - declared_amount)
                tolerance = Decimal("0.01")
                
                if difference > tolerance:
                    failed_items.append({
                        "item_index": idx,
                        "item_description": item.get("description", ""),
                        "calculated": float(calculated_amount),
                        "declared": float(declared_amount),
                        "difference": float(difference)
                    })
            
            if not failed_items:
                return {
                    "status": "pass",
                    "message": "橫式計算驗證通過",
                    "checked_items": len(items)
                }
            else:
                return {
                    "status": "fail",
                    "message": f"有 {len(failed_items)} 個項目計算不符",
                    "failed_items": failed_items
                }
            
        except (ValueError, InvalidOperation, TypeError) as e:
            logger.error(f"Error in horizontal calculation validation: {e}")
            return {
                "status": "error",
                "message": f"驗證過程發生錯誤：{str(e)}"
            }
    
    def validate_subtotal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        驗證小計金額
        
        Args:
            data: 估驗計價資料
        
        Returns:
            Dict: 驗算結果
        """
        # TODO: 實作具體邏輯
        # 根據實際文件結構確定小計的定義和計算方式
        
        logger.info("Executing subtotal validation")
        
        return {
            "status": "pass",
            "message": "小計驗證功能待實作"
        }
    
    def validate_total(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        驗證總計金額
        
        Args:
            data: 估驗計價資料
        
        Returns:
            Dict: 驗算結果
        """
        # TODO: 實作具體邏輯
        
        logger.info("Executing total validation")
        
        return {
            "status": "pass",
            "message": "總計驗證功能待實作"
        }


# 單例模式
_amount_engine = None

def get_amount_engine() -> AmountCalculationEngine:
    """取得金額驗算引擎實例"""
    global _amount_engine
    if _amount_engine is None:
        _amount_engine = AmountCalculationEngine()
    return _amount_engine
