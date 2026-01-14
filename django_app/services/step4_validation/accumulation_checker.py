"""
累計檢核模組
處理前後期累計金額的檢核邏輯

TODO: 待有實際文件範本後實作具體檢核規則
"""
import logging
from typing import Dict, Any, List, Optional
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)


class AccumulationChecker:
    """
    累計檢核器
    負責驗證累計金額的正確性
    """
    
    def validate_all(
        self,
        current_period: Dict[str, Any],
        previous_periods: Optional[List[Dict[str, Any]]] = None,
        contract_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        執行所有累計檢核
        
        Args:
            current_period: 本期資料
            previous_periods: 前期資料列表
            contract_info: 合約資訊
        
        Returns:
            Dict: 檢核結果
        """
        results = {
            "accumulation_logic": self.check_accumulation_logic(
                current_period, previous_periods
            ),
            "contract_limit": self.check_contract_limit(
                current_period, contract_info
            ),
            "progress_check": self.check_progress_reasonability(
                current_period, previous_periods, contract_info
            )
        }
        
        # 判斷整體是否通過
        all_passed = all(
            result.get("status") in ["pass", "warning"]
            for result in results.values()
        )
        
        results["overall_status"] = "pass" if all_passed else "fail"
        
        return results
    
    def check_accumulation_logic(
        self,
        current_period: Dict[str, Any],
        previous_periods: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        檢核累計邏輯：前期累計 + 本期金額 = 本期累計
        
        Args:
            current_period: 本期資料
            previous_periods: 前期資料列表
        
        Returns:
            Dict: 檢核結果
        """
        # TODO: 實作具體邏輯
        # 需要根據實際文件範本確定：
        # 1. 累計金額的欄位名稱
        # 2. 本期金額的欄位名稱
        # 3. 如何追蹤歷史資料
        
        logger.info("Checking accumulation logic")
        
        try:
            # 框架邏輯示例
            if not previous_periods or len(previous_periods) == 0:
                # 第一期
                return {
                    "status": "pass",
                    "message": "第一期資料，無前期累計",
                    "period_number": current_period.get("period_number", 1)
                }
            
            # 取得前期累計
            prev_total = Decimal(str(
                previous_periods[-1].get("current_accumulation", 0)
            ))
            
            # 本期金額
            current_amount = Decimal(str(
                current_period.get("period_amount", 0)
            ))
            
            # 本期累計（聲明值）
            declared_total = Decimal(str(
                current_period.get("current_accumulation", 0)
            ))
            
            # 計算值
            calculated_total = prev_total + current_amount
            
            # 比對
            difference = abs(calculated_total - declared_total)
            tolerance = Decimal("0.01")
            
            if difference <= tolerance:
                return {
                    "status": "pass",
                    "message": "累計邏輯檢核通過",
                    "previous_total": float(prev_total),
                    "current_amount": float(current_amount),
                    "calculated_total": float(calculated_total),
                    "declared_total": float(declared_total),
                    "difference": float(difference)
                }
            else:
                return {
                    "status": "fail",
                    "message": f"累計邏輯不符：差異 {difference}",
                    "previous_total": float(prev_total),
                    "current_amount": float(current_amount),
                    "calculated_total": float(calculated_total),
                    "declared_total": float(declared_total),
                    "difference": float(difference)
                }
            
        except (ValueError, InvalidOperation, TypeError) as e:
            logger.error(f"Error in accumulation logic check: {e}")
            return {
                "status": "error",
                "message": f"檢核過程發生錯誤：{str(e)}"
            }
    
    def check_contract_limit(
        self,
        current_period: Dict[str, Any],
        contract_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        檢核合約總額上限
        確保累計金額不超過合約總額
        
        Args:
            current_period: 本期資料
            contract_info: 合約資訊 (可以是 contract_info 或 contract_financials)
        
        Returns:
            Dict: 檢核結果
        """
        # TODO: 實作具體邏輯
        
        logger.info("Checking contract limit")
        
        try:
            if not contract_info:
                return {
                    "status": "warning",
                    "message": "無合約資訊，無法檢核上限"
                }
            
            # 兼容新舊 Schema
            # 新 Schema: current_total_amount (變更後契約金額)
            # 舊 Schema: contract_amount
            contract_amount = Decimal(str(
                contract_info.get("current_total_amount") or 
                contract_info.get("contract_amount", 0)
            ))
            
            current_total = Decimal(str(
                current_period.get("current_accumulation", 0)
            ))
            
            if current_total > contract_amount:
                return {
                    "status": "fail",
                    "message": "累計金額超過合約總額",
                    "contract_amount": float(contract_amount),
                    "current_total": float(current_total),
                    "exceeded_amount": float(current_total - contract_amount)
                }
            else:
                remaining = contract_amount - current_total
                usage_percentage = (current_total / contract_amount * 100) if contract_amount > 0 else 0
                
                return {
                    "status": "pass",
                    "message": "未超過合約總額",
                    "contract_amount": float(contract_amount),
                    "current_total": float(current_total),
                    "remaining_amount": float(remaining),
                    "usage_percentage": float(usage_percentage)
                }
            
        except (ValueError, InvalidOperation, TypeError) as e:
            logger.error(f"Error in contract limit check: {e}")
            return {
                "status": "error",
                "message": f"檢核過程發生錯誤：{str(e)}"
            }
    
    def check_progress_reasonability(
        self,
        current_period: Dict[str, Any],
        previous_periods: Optional[List[Dict[str, Any]]] = None,
        contract_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        檢核進度合理性
        分析進度是否異常（過快或過慢）
        
        Args:
            current_period: 本期資料
            previous_periods: 前期資料列表
            contract_info: 合約資訊
        
        Returns:
            Dict: 檢核結果
        """
        # TODO: 實作具體邏輯
        # 需要定義何謂「合理」的進度
        
        logger.info("Checking progress reasonability")
        
        return {
            "status": "pass",
            "message": "進度合理性檢核功能待實作"
        }
    
    def get_historical_trend(
        self,
        periods: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        分析歷史趨勢
        提供累計金額的趨勢分析
        
        Args:
            periods: 各期資料列表
        
        Returns:
            Dict: 趨勢分析結果
        """
        # TODO: 實作趨勢分析
        
        logger.info("Analyzing historical trend")
        
        return {
            "total_periods": len(periods),
            "trend": "待實作"
        }


# 單例模式
_accumulation_checker = None

def get_accumulation_checker() -> AccumulationChecker:
    """取得累計檢核器實例"""
    global _accumulation_checker
    if _accumulation_checker is None:
        _accumulation_checker = AccumulationChecker()
    return _accumulation_checker
