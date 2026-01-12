"""
Model Optimizer
模型優化器

基於回饋資料優化 AI 模型和規則
"""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ModelOptimizer:
    """
    模型優化器
    負責優化 GPT Prompts、驗算規則等
    """
    
    def optimize_from_feedback(
        self,
        feedback_records: List[Dict[str, Any]],
        optimization_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        基於回饋記錄優化模型
        
        Args:
            feedback_records: 回饋記錄列表
            optimization_config: 優化配置
        
        Returns:
            Dict: 優化結果
        """
        logger.info(f"Starting optimization with {len(feedback_records)} feedback records")
        
        try:
            results = {
                "optimized_at": datetime.now().isoformat(),
                "improvements": []
            }
            
            # 1. 優化 Prompt 模板
            prompt_improvements = self._optimize_prompts(feedback_records)
            if prompt_improvements:
                results["improvements"].append({
                    "type": "prompt",
                    "changes": prompt_improvements
                })
            
            # 2. 優化驗算規則
            rule_improvements = self._optimize_rules(feedback_records)
            if rule_improvements:
                results["improvements"].append({
                    "type": "validation_rule",
                    "changes": rule_improvements
                })
            
            # 3. 更新信心分數權重
            confidence_improvements = self._optimize_confidence_weights(feedback_records)
            if confidence_improvements:
                results["improvements"].append({
                    "type": "confidence_weight",
                    "changes": confidence_improvements
                })
            
            logger.info(f"Optimization completed with {len(results['improvements'])} improvements")
            return results
            
        except Exception as e:
            logger.error(f"Error during optimization: {e}")
            raise
    
    def _optimize_prompts(
        self,
        feedback_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        優化 Prompt 模板
        
        Args:
            feedback_records: 回饋記錄
        
        Returns:
            List[Dict]: Prompt 改進列表
        """
        improvements = []
        
        # 分析常見錯誤模式
        error_patterns = self._analyze_error_patterns(feedback_records)
        
        # 針對每個錯誤模式提出 Prompt 改進
        for pattern in error_patterns:
            if pattern["frequency"] >= 5:  # 至少出現 5 次
                improvement = {
                    "pattern": pattern["description"],
                    "current_prompt": pattern["related_prompt"],
                    "suggested_improvement": self._suggest_prompt_improvement(pattern),
                    "priority": "high" if pattern["frequency"] >= 10 else "medium"
                }
                improvements.append(improvement)
        
        logger.info(f"Generated {len(improvements)} prompt improvements")
        return improvements
    
    def _optimize_rules(
        self,
        feedback_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        優化驗算規則
        
        Args:
            feedback_records: 回饋記錄
        
        Returns:
            List[Dict]: 規則改進列表
        """
        improvements = []
        
        # 識別驗算錯誤
        validation_errors = [
            rec for rec in feedback_records 
            if rec.get("error_type") == "validation"
        ]
        
        if not validation_errors:
            return improvements
        
        # 按驗算類型分組
        errors_by_type = {}
        for error in validation_errors:
            v_type = error.get("validation_type", "unknown")
            if v_type not in errors_by_type:
                errors_by_type[v_type] = []
            errors_by_type[v_type].append(error)
        
        # 針對每種類型提出改進建議
        for v_type, errors in errors_by_type.items():
            if len(errors) >= 3:  # 至少 3 個錯誤
                improvement = {
                    "validation_type": v_type,
                    "error_count": len(errors),
                    "suggested_adjustment": self._suggest_rule_adjustment(v_type, errors),
                    "priority": "high" if len(errors) >= 5 else "medium"
                }
                improvements.append(improvement)
        
        logger.info(f"Generated {len(improvements)} rule improvements")
        return improvements
    
    def _optimize_confidence_weights(
        self,
        feedback_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        優化信心分數權重
        
        Args:
            feedback_records: 回饋記錄
        
        Returns:
            Dict: 權重調整建議
        """
        # TODO: 實作權重優化邏輯
        # 基於實際準確度調整各模組的權重
        
        return {
            "current_weights": {
                "icr": 0.3,
                "mapping": 0.4,
                "validation": 0.3
            },
            "suggested_weights": {
                "icr": 0.3,
                "mapping": 0.4,
                "validation": 0.3
            },
            "reason": "待收集更多資料後調整"
        }
    
    def _analyze_error_patterns(
        self,
        feedback_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        分析錯誤模式
        
        Args:
            feedback_records: 回饋記錄
        
        Returns:
            List[Dict]: 錯誤模式列表
        """
        patterns = []
        
        # 按欄位名稱分組
        errors_by_field = {}
        for record in feedback_records:
            if record.get("feedback_type") in ["incorrect", "partial"]:
                field = record.get("field_name", "unknown")
                if field not in errors_by_field:
                    errors_by_field[field] = []
                errors_by_field[field].append(record)
        
        # 生成模式描述
        for field, errors in errors_by_field.items():
            if len(errors) >= 3:
                pattern = {
                    "field": field,
                    "frequency": len(errors),
                    "description": f"欄位 '{field}' 經常識別錯誤",
                    "related_prompt": "field_extraction",
                    "examples": errors[:3]  # 保留前 3 個範例
                }
                patterns.append(pattern)
        
        return patterns
    
    def _suggest_prompt_improvement(
        self,
        error_pattern: Dict[str, Any]
    ) -> str:
        """
        建議 Prompt 改進
        
        Args:
            error_pattern: 錯誤模式
        
        Returns:
            str: 改進建議
        """
        field = error_pattern["field"]
        
        suggestions = {
            "amount": "加強金額格式說明，強調需移除千分位符號",
            "date": "提供多種日期格式範例，包括民國年轉換說明",
            "quantity": "明確說明數量欄位可能包含小數點",
            "default": f"針對 '{field}' 欄位提供更明確的識別指示和範例"
        }
        
        return suggestions.get(field, suggestions["default"])
    
    def _suggest_rule_adjustment(
        self,
        validation_type: str,
        errors: List[Dict[str, Any]]
    ) -> str:
        """
        建議規則調整
        
        Args:
            validation_type: 驗算類型
            errors: 錯誤列表
        
        Returns:
            str: 調整建議
        """
        suggestions = {
            "amount": "放寬金額誤差容忍度至 0.1 元",
            "accumulation": "檢查累計邏輯是否考慮了扣款情況",
            "payment_condition": "優化付款條件解析的正則表達式",
            "default": f"檢視 {validation_type} 驗算的容錯機制"
        }
        
        return suggestions.get(validation_type, suggestions["default"])
    
    def schedule_optimization(
        self,
        schedule_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        排程定期優化
        
        Args:
            schedule_config: 排程配置
        
        Returns:
            Dict: 排程資訊
        """
        # TODO: 整合排程系統（如 Celery Beat）
        
        if schedule_config is None:
            schedule_config = {
                "frequency": "weekly",
                "min_feedback_count": 50
            }
        
        logger.info(f"Optimization scheduled with config: {schedule_config}")
        
        return {
            "scheduled": True,
            "next_run": (datetime.now() + timedelta(days=7)).isoformat(),
            "config": schedule_config
        }


# 單例模式
_model_optimizer = None

def get_model_optimizer() -> ModelOptimizer:
    """取得模型優化器實例"""
    global _model_optimizer
    if _model_optimizer is None:
        _model_optimizer = ModelOptimizer()
    return _model_optimizer
