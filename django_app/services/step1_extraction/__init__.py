"""
Step 1: Data Extraction
文件掃描與資料擷取模組

使用 Azure Document Intelligence 進行 ICR (智能字元識別)
"""
from .azure_di_service import AzureDocumentIntelligenceService, get_azure_di_service
from .pdf_handler import PDFHandler

__all__ = [
    'AzureDocumentIntelligenceService',
    'get_azure_di_service',
    'PDFHandler',
]
