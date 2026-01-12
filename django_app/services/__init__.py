"""
Services Layer
服務層模組

嚴格遵循 5 步驟流程架構：
1. Data Extraction (step1_extraction/) - ICR 資料擷取
2. Context Understanding (step2_understanding/) - GPT-5 語義理解
3. Standardization (step3_standardization/) - 資料標準化
4. Validation Engine (step4_validation/) - 自動驗算引擎
5. Feedback Loop (step5_feedback/) - 回饋與優化

Common (common/) - 共用工具模組
"""

# Step 1: Data Extraction
from .step1_extraction import (
    AzureDocumentIntelligenceService,
    get_azure_di_service,
    PDFHandler
)

# Step 2: Context Understanding
from .step2_understanding import (
    AzureGPTService,
    get_azure_gpt_service
)

# Step 3: Standardization
from .step3_standardization import (
    DataNormalizer,
    get_data_normalizer,
    SchemaValidator,
    get_schema_validator
)

# Step 4: Validation Engine
from .step4_validation import (
    AmountCalculationEngine,
    get_amount_engine,
    AccumulationChecker,
    get_accumulation_checker,
    PaymentConditionEngine,
    get_payment_engine,
    RulesEngine,
    get_rules_engine
)

# Step 5: Feedback Loop
from .step5_feedback import (
    FeedbackProcessor,
    get_feedback_processor,
    ModelOptimizer,
    get_model_optimizer
)

# Common Utilities
from .common import (
    ConfidenceCalculator,
    ErrorHandler,
    ValidationError,
    ProcessingError
)

__all__ = [
    # Step 1
    'AzureDocumentIntelligenceService',
    'get_azure_di_service',
    'PDFHandler',
    
    # Step 2
    'AzureGPTService',
    'get_azure_gpt_service',
    
    # Step 3
    'DataNormalizer',
    'get_data_normalizer',
    'SchemaValidator',
    'get_schema_validator',
    
    # Step 4
    'AmountCalculationEngine',
    'get_amount_engine',
    'AccumulationChecker',
    'get_accumulation_checker',
    'PaymentConditionEngine',
    'get_payment_engine',
    'RulesEngine',
    'get_rules_engine',
    
    # Step 5
    'FeedbackProcessor',
    'get_feedback_processor',
    'ModelOptimizer',
    'get_model_optimizer',
    
    # Common
    'ConfidenceCalculator',
    'ErrorHandler',
    'ValidationError',
    'ProcessingError',
]
