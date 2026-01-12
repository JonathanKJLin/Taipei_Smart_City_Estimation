"""
Document Processor Celery Tasks
異步處理任務
"""
import logging
from celery import shared_task
from django.utils import timezone

from .models import Document, ProcessingLog
from django_app.services.base.azure_di_service import get_azure_di_service
from django_app.services.base.azure_gpt_service import get_azure_gpt_service
from django_app.services.estimation.amount_engine import get_amount_engine
from django_app.services.estimation.accumulation_checker import get_accumulation_checker
from django_app.services.estimation.payment_condition_engine import get_payment_engine

logger = logging.getLogger(__name__)


@shared_task
def process_document_task(document_id: int):
    """
    處理文件的異步任務
    
    Args:
        document_id: 文件 ID
    """
    try:
        document = Document.objects.get(id=document_id)
        document.status = 'processing'
        document.save()
        
        _log(document, 'started', '開始處理文件')
        
        # Step 1: ICR 掃描
        _log(document, 'icr', '執行 ICR 智能字元識別')
        di_service = get_azure_di_service()
        icr_result = di_service.analyze_document(document.file_path)
        document.icr_result = icr_result
        document.save()
        
        # Step 2: GPT 語義理解與欄位對應
        _log(document, 'gpt_processing', '執行 GPT 語義理解')
        gpt_service = get_azure_gpt_service()
        # TODO: 載入對應的 prompt 模板
        structured_data = gpt_service.understand_field_mapping(
            icr_data=icr_result,
            target_schema={}  # TODO: 根據文件類型選擇 schema
        )
        document.structured_data = structured_data
        document.save()
        
        # Step 3: 執行驗算
        _log(document, 'validation', '執行驗算檢核')
        
        # 金額驗算
        amount_engine = get_amount_engine()
        amount_results = amount_engine.validate_all(structured_data)
        
        # 累計檢核
        accumulation_checker = get_accumulation_checker()
        accumulation_results = accumulation_checker.validate_all(
            current_period=structured_data,
            previous_periods=None,  # TODO: 查詢歷史資料
            contract_info=structured_data.get('contract_info')
        )
        
        # 付款條件驗證
        payment_engine = get_payment_engine()
        payment_conditions = payment_engine.extract_conditions_from_document(structured_data)
        
        # 彙整驗算結果
        validation_result = {
            'amount_validation': amount_results,
            'accumulation_validation': accumulation_results,
            'payment_conditions': payment_conditions,
            'timestamp': timezone.now().isoformat()
        }
        
        document.validation_result = validation_result
        document.save()
        
        # Step 4: 計算信心分數
        _log(document, 'confidence', '計算信心分數')
        # TODO: 實作信心分數計算
        document.confidence_score = 0.85  # 暫時值
        
        # 完成
        document.status = 'completed'
        document.processed_at = timezone.now()
        document.save()
        
        _log(document, 'completed', '文件處理完成')
        
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {e}")
        
        try:
            document = Document.objects.get(id=document_id)
            document.status = 'failed'
            document.error_message = str(e)
            document.save()
            
            _log(document, 'error', f'處理失敗：{str(e)}')
        except:
            pass
        
        raise


def _log(document: Document, stage: str, message: str, details: dict = None):
    """記錄處理日誌"""
    ProcessingLog.objects.create(
        document=document,
        stage=stage,
        message=message,
        details=details
    )
    logger.info(f"[{document.document_id}] {stage}: {message}")
