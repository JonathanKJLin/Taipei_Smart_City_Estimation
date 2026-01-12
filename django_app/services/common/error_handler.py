"""
Error Handler
錯誤處理器

統一的錯誤處理和日誌記錄
"""
import logging
import traceback
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """驗證錯誤"""
    pass


class ProcessingError(Exception):
    """處理錯誤"""
    pass


class ErrorHandler:
    """
    錯誤處理器
    提供統一的錯誤處理、日誌記錄和錯誤回報機制
    """
    
    @staticmethod
    def handle_exception(
        exception: Exception,
        context: Dict[str, Any] = None,
        severity: str = "error"
    ) -> Dict[str, Any]:
        """
        處理異常
        
        Args:
            exception: 異常物件
            context: 上下文資訊
            severity: 嚴重程度 (debug, info, warning, error, critical)
        
        Returns:
            Dict: 錯誤資訊
        """
        error_info = {
            "error_type": type(exception).__name__,
            "error_message": str(exception),
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "context": context or {}
        }
        
        # 記錄詳細的追蹤資訊
        if severity in ["error", "critical"]:
            error_info["traceback"] = traceback.format_exc()
        
        # 記錄日誌
        log_method = getattr(logger, severity, logger.error)
        log_message = f"{error_info['error_type']}: {error_info['error_message']}"
        
        if context:
            log_message += f" | Context: {context}"
        
        log_method(log_message)
        
        # 對於嚴重錯誤，可能需要通知管理員
        if severity == "critical":
            ErrorHandler._notify_admin(error_info)
        
        return error_info
    
    @staticmethod
    def wrap_with_error_handling(func):
        """
        裝飾器：為函數添加錯誤處理
        
        Args:
            func: 要包裝的函數
        
        Returns:
            包裝後的函數
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    "function": func.__name__,
                    "args": str(args)[:100],  # 限制長度
                    "kwargs": str(kwargs)[:100]
                }
                error_info = ErrorHandler.handle_exception(e, context)
                raise ProcessingError(
                    f"Error in {func.__name__}: {error_info['error_message']}"
                )
        
        return wrapper
    
    @staticmethod
    def validate_data(
        data: Any,
        validation_func: callable,
        error_message: str = "資料驗證失敗"
    ):
        """
        驗證資料
        
        Args:
            data: 待驗證的資料
            validation_func: 驗證函數（返回 bool）
            error_message: 錯誤訊息
        
        Raises:
            ValidationError: 驗證失敗時
        """
        try:
            if not validation_func(data):
                raise ValidationError(error_message)
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"{error_message}: {str(e)}")
    
    @staticmethod
    def log_processing_step(
        step_name: str,
        document_id: str = None,
        details: Dict[str, Any] = None
    ):
        """
        記錄處理步驟
        
        Args:
            step_name: 步驟名稱
            document_id: 文件編號
            details: 詳細資訊
        """
        log_message = f"[{step_name}]"
        
        if document_id:
            log_message += f" Document: {document_id}"
        
        if details:
            log_message += f" | {details}"
        
        logger.info(log_message)
    
    @staticmethod
    def create_error_response(
        error_info: Dict[str, Any],
        user_friendly: bool = True
    ) -> Dict[str, Any]:
        """
        創建錯誤回應
        
        Args:
            error_info: 錯誤資訊
            user_friendly: 是否返回使用者友善的訊息
        
        Returns:
            Dict: 錯誤回應
        """
        if user_friendly:
            # 使用者友善的錯誤訊息
            user_messages = {
                "ValidationError": "資料驗證失敗，請檢查輸入資料",
                "ProcessingError": "處理過程發生錯誤，請稍後重試",
                "ConnectionError": "連接失敗，請檢查網路連線",
                "TimeoutError": "請求逾時，請稍後重試"
            }
            
            error_type = error_info["error_type"]
            user_message = user_messages.get(error_type, "發生未預期的錯誤")
            
            return {
                "success": False,
                "error": user_message,
                "error_code": error_type,
                "timestamp": error_info["timestamp"]
            }
        else:
            # 詳細的錯誤資訊（用於除錯）
            return {
                "success": False,
                "error": error_info
            }
    
    @staticmethod
    def _notify_admin(error_info: Dict[str, Any]):
        """
        通知管理員嚴重錯誤
        
        Args:
            error_info: 錯誤資訊
        """
        # TODO: 實作通知機制（Email、Slack 等）
        logger.critical(
            f"CRITICAL ERROR - Admin notification: {error_info['error_type']}"
        )
    
    @staticmethod
    def get_error_statistics(
        time_period: str = "last_24h"
    ) -> Dict[str, Any]:
        """
        取得錯誤統計
        
        Args:
            time_period: 時間區間
        
        Returns:
            Dict: 統計資訊
        """
        # TODO: 實作錯誤統計邏輯
        # 可以從日誌或資料庫中統計
        
        return {
            "period": time_period,
            "total_errors": 0,
            "errors_by_type": {},
            "errors_by_severity": {}
        }
