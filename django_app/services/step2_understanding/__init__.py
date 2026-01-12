"""
Step 2: Context Understanding
語義理解與邏輯識別模組

使用 GPT-5 進行 NLP 分析
"""
from .gpt_service import AzureGPTService, get_azure_gpt_service

__all__ = [
    'AzureGPTService',
    'get_azure_gpt_service',
]
