"""
Document Processor Celery Tasks
異步處理任務

遵循 5 步流程架構
"""
import logging
from celery import shared_task
from django.utils import timezone

from .models import Document, ProcessingLog

# Step 1: Data Extraction
from django_app.services.step1_extraction import get_azure_di_service

# Step 2: Context Understanding
from django_app.services.step2_understanding import get_azure_gpt_service

# Step 3: Standardization
from django_app.services.step3_standardization import (
    get_data_normalizer,
    get_schema_validator
)

# Step 4: Validation Engine
from django_app.services.step4_validation import (
    get_amount_engine,
    get_accumulation_checker,
    get_payment_engine
)

# Step 5: Feedback Loop (for future use)
# from django_app.services.step5_feedback import get_feedback_processor

# Common utilities
from django_app.services.common import ConfidenceCalculator, ErrorHandler

logger = logging.getLogger(__name__)


@shared_task
def process_document_task(document_id: int):
    """
    處理文件的異步任務
    嚴格遵循 5 步流程
    
    Args:
        document_id: 文件 ID
    """
    try:
        document = Document.objects.get(id=document_id)
        document.status = 'processing'
        document.save()
        
        _log(document, 'started', '開始處理文件 - 啟動 5 步流程')
        
        # ==================== Step 1: Data Extraction ====================
        _log(document, 'step1_extraction', 'Step 1: 執行資料擷取 (ICR)')
        
        di_service = get_azure_di_service()
        icr_result = di_service.analyze_document(document.file_path)
        document.icr_result = icr_result
        document.save()
        
        _log(document, 'step1_completed', 'Step 1 完成：ICR 資料擷取成功')
        
        # ==================== Step 2: Context Understanding ====================
        _log(document, 'step2_understanding', 'Step 2: 執行語義理解 (GPT-5 NLP)')
        
        gpt_service = get_azure_gpt_service()
        
        # TODO: 根據文件類型選擇適當的 Schema
        from django_app.schemas.estimation_schema import ESTIMATION_PAYMENT_SCHEMA
        target_schema = ESTIMATION_PAYMENT_SCHEMA
        
        understood_data = gpt_service.understand_field_mapping(
            icr_data=icr_result,
            target_schema=target_schema
        )
        
        _log(document, 'step2_completed', 'Step 2 完成：語義理解與欄位對應成功')
        
        # ==================== Step 3: Standardization ====================
        _log(document, 'step3_standardization', 'Step 3: 執行資料標準化')
        
        data_normalizer = get_data_normalizer()
        standardized_data = data_normalizer.normalize_document(
            raw_data=understood_data,
            document_type=document.document_type
        )
        
        # 驗證 Schema
        schema_validator = get_schema_validator()
        is_valid, validation_errors = schema_validator.validate(
            data=standardized_data,
            schema=target_schema
        )
        
        if not is_valid:
            _log(document, 'step3_warning', 
                 f'Schema 驗證警告：{len(validation_errors)} 個問題',
                 {'errors': validation_errors})
        
        document.structured_data = standardized_data
        document.save()
        
        _log(document, 'step3_completed', 'Step 3 完成：資料標準化處理完成')
        
        # ==================== Step 4: Validation Engine ====================
        _log(document, 'step4_validation', 'Step 4: 執行自動驗算引擎')
        
        validation_results = {}
        
        # 4.1 金額驗算
        amount_engine = get_amount_engine()
        validation_results['amount_validation'] = amount_engine.validate_all(
            standardized_data
        )
        
        # 4.2 累計檢核
        accumulation_checker = get_accumulation_checker()
        validation_results['accumulation_validation'] = accumulation_checker.validate_all(
            current_period=standardized_data,
            previous_periods=None,  # TODO: 查詢歷史資料
            contract_info=standardized_data.get('contract_info')
        )
        
        # 4.3 付款條件驗證
        payment_engine = get_payment_engine()
        payment_conditions = payment_engine.extract_conditions_from_document(
            standardized_data
        )
        validation_results['payment_conditions'] = payment_conditions
        
        # 彙整驗算結果
        validation_result = {
            **validation_results,
            'timestamp': timezone.now().isoformat(),
            'version': '1.0'
        }
        
        document.validation_result = validation_result
        document.save()
        
        _log(document, 'step4_completed', 'Step 4 完成：自動驗算執行完成')
        
        # ==================== 計算信心分數 ====================
        _log(document, 'confidence_calculation', '計算整體信心分數')
        
        calculator = ConfidenceCalculator()
        
        icr_confidence = calculator.calculate_icr_confidence(icr_result)
        
        # TODO: 完善欄位對應和驗算的信心分數計算
        mapping_confidence = 0.90  # 暫時值
        validation_confidence = calculator.calculate_validation_confidence(
            validation_results
        )
        
        overall_confidence = calculator.calculate_overall_confidence(
            icr_confidence=icr_confidence,
            mapping_confidence=mapping_confidence,
            validation_confidence=validation_confidence
        )
        
        document.confidence_score = overall_confidence
        
        # ==================== 完成 ====================
        document.status = 'completed'
        document.processed_at = timezone.now()
        document.save()
        
        _log(document, 'completed', 
             f'✅ 文件處理完成 (信心分數: {overall_confidence:.2%})',
             {
                 'icr_confidence': icr_confidence,
                 'mapping_confidence': mapping_confidence,
                 'validation_confidence': validation_confidence,
                 'overall_confidence': overall_confidence
             })
        
        # Note: Step 5 (Feedback Loop) 將在人工審核後觸發
        
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {e}")
        
        try:
            document = Document.objects.get(id=document_id)
            document.status = 'failed'
            
            # 使用 ErrorHandler 處理錯誤
            error_info = ErrorHandler.handle_exception(
                e,
                context={'document_id': document_id, 'document_type': document.document_type},
                severity='error'
            )
            document.error_message = error_info['error_message']
            document.save()
            
            _log(document, 'error', f'❌ 處理失敗：{error_info["error_message"]}')
        except:
            pass
        
        raise


def _log(document: Document, stage: str, message: str, details: dict = None):
    """
    記錄處理日誌
    
    Args:
        document: 文件物件
        stage: 處理階段
        message: 訊息
        details: 詳細資訊
    """
    ProcessingLog.objects.create(
        document=document,
        stage=stage,
        message=message,
        details=details
    )
    logger.info(f"[{document.document_id}] {stage}: {message}")
