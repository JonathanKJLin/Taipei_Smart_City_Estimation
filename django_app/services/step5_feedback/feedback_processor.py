"""
Feedback Processor
回饋處理器

收集並處理人工回饋，用於優化系統
"""
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackProcessor:
    """
    回饋處理器
    處理人工審核的回饋資訊
    """
    
    def process_feedback(
        self,
        document_id: str,
        feedback_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        處理回饋資料
        
        Args:
            document_id: 文件編號
            feedback_data: 回饋資料
        
        Returns:
            Dict: 處理結果
        """
        logger.info(f"Processing feedback for document: {document_id}")
        
        try:
            # 儲存回饋記錄
            feedback_record = self._save_feedback(document_id, feedback_data)
            
            # 分析回饋
            analysis = self._analyze_feedback(feedback_data)
            
            # 識別需要改進的領域
            improvement_areas = self._identify_improvement_areas(feedback_data)
            
            # 觸發模型優化
            if improvement_areas:
                self._trigger_optimization(improvement_areas)
            
            result = {
                "feedback_id": feedback_record.get("id"),
                "processed_at": datetime.now().isoformat(),
                "analysis": analysis,
                "improvement_areas": improvement_areas,
                "status": "processed"
            }
            
            logger.info(f"Feedback processed successfully: {result['feedback_id']}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            raise
    
    def _save_feedback(
        self,
        document_id: str,
        feedback_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        儲存回饋記錄到資料庫
        
        Args:
            document_id: 文件編號
            feedback_data: 回饋資料
        
        Returns:
            Dict: 儲存的記錄
        """
        # TODO: 整合 Django Models
        from django_app.apps.estimation_validator.models import FeedbackRecord
        
        try:
            records = []
            
            # 處理欄位級別的回饋
            if "field_corrections" in feedback_data:
                for correction in feedback_data["field_corrections"]:
                    record = FeedbackRecord.objects.create(
                        document_id=document_id,
                        field_name=correction.get("field_name"),
                        system_value=correction.get("system_value"),
                        correct_value=correction.get("correct_value"),
                        feedback_type=correction.get("feedback_type", "incorrect"),
                        comment=correction.get("comment", "")
                    )
                    records.append(record)
            
            # 處理整體回饋
            if "overall_feedback" in feedback_data:
                record = FeedbackRecord.objects.create(
                    document_id=document_id,
                    field_name="overall",
                    system_value=feedback_data.get("system_result"),
                    correct_value=feedback_data.get("overall_feedback"),
                    feedback_type="overall",
                    comment=feedback_data.get("comment", "")
                )
                records.append(record)
            
            logger.info(f"Saved {len(records)} feedback records")
            return {"id": records[0].id if records else None, "count": len(records)}
            
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
            return {"id": None, "count": 0}
    
    def _analyze_feedback(
        self,
        feedback_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        分析回饋資料
        
        Args:
            feedback_data: 回饋資料
        
        Returns:
            Dict: 分析結果
        """
        analysis = {
            "total_corrections": 0,
            "error_types": {},
            "accuracy_impact": 0.0
        }
        
        # 統計修正數量
        if "field_corrections" in feedback_data:
            analysis["total_corrections"] = len(feedback_data["field_corrections"])
            
            # 按錯誤類型分類
            for correction in feedback_data["field_corrections"]:
                error_type = correction.get("error_type", "unknown")
                analysis["error_types"][error_type] = analysis["error_types"].get(error_type, 0) + 1
        
        # 計算對準確度的影響
        if analysis["total_corrections"] > 0:
            # 簡單估算：每個錯誤降低 2% 準確度
            analysis["accuracy_impact"] = min(analysis["total_corrections"] * 0.02, 1.0)
        
        return analysis
    
    def _identify_improvement_areas(
        self,
        feedback_data: Dict[str, Any]
    ) -> List[str]:
        """
        識別需要改進的領域
        
        Args:
            feedback_data: 回饋資料
        
        Returns:
            List[str]: 改進領域列表
        """
        improvement_areas = []
        
        if "field_corrections" in feedback_data:
            # 按欄位分組統計錯誤
            field_errors = {}
            for correction in feedback_data["field_corrections"]:
                field = correction.get("field_name")
                field_errors[field] = field_errors.get(field, 0) + 1
            
            # 識別高錯誤率的欄位
            for field, count in field_errors.items():
                if count >= 3:  # 閾值：3次以上錯誤
                    improvement_areas.append(f"field_extraction:{field}")
        
        # 檢查驗算錯誤
        if "validation_errors" in feedback_data:
            for error in feedback_data["validation_errors"]:
                validation_type = error.get("type")
                improvement_areas.append(f"validation:{validation_type}")
        
        return improvement_areas
    
    def _trigger_optimization(
        self,
        improvement_areas: List[str]
    ):
        """
        觸發模型優化
        
        Args:
            improvement_areas: 需要改進的領域
        """
        logger.info(f"Triggering optimization for areas: {improvement_areas}")
        
        # TODO: 實作實際的優化觸發邏輯
        # 可能包括：
        # - 更新 Prompt 模板
        # - 調整驗算規則
        # - 微調 GPT 模型
        # - 更新規則庫
        
        pass
    
    def get_feedback_statistics(
        self,
        time_period: str = "last_month"
    ) -> Dict[str, Any]:
        """
        取得回饋統計資訊
        
        Args:
            time_period: 時間區間
        
        Returns:
            Dict: 統計資訊
        """
        # TODO: 實作統計邏輯
        from django_app.apps.estimation_validator.models import FeedbackRecord
        
        try:
            # 基本統計
            total_feedbacks = FeedbackRecord.objects.count()
            
            # 按類型統計
            feedback_by_type = {}
            for feedback_type in ['correct', 'incorrect', 'partial']:
                count = FeedbackRecord.objects.filter(
                    feedback_type=feedback_type
                ).count()
                feedback_by_type[feedback_type] = count
            
            stats = {
                "total_feedbacks": total_feedbacks,
                "feedback_by_type": feedback_by_type,
                "period": time_period
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting feedback statistics: {e}")
            return {}


# 單例模式
_feedback_processor = None

def get_feedback_processor() -> FeedbackProcessor:
    """取得回饋處理器實例"""
    global _feedback_processor
    if _feedback_processor is None:
        _feedback_processor = FeedbackProcessor()
    return _feedback_processor
