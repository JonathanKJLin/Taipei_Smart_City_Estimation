"""
Azure Document Intelligence Service
處理文件掃描、ICR（智能字元識別）、表格識別等功能

從 AZTL 專案重用並修改
"""
import logging
from typing import Dict, Any, List
from django.conf import settings

logger = logging.getLogger(__name__)


class AzureDocumentIntelligenceService:
    """
    Azure Document Intelligence 服務封裝
    提供文件分析、ICR（智能字元識別）、表格擷取等功能
    """
    
    def __init__(self):
        """初始化 Azure DI 客戶端"""
        self.endpoint = settings.AZURE_DI_ENDPOINT
        self.key = settings.AZURE_DI_KEY
        self.client = None
        
        if self.endpoint and self.key:
            try:
                from azure.ai.documentintelligence import DocumentIntelligenceClient
                from azure.core.credentials import AzureKeyCredential
                
                self.client = DocumentIntelligenceClient(
                    endpoint=self.endpoint,
                    credential=AzureKeyCredential(self.key)
                )
                logger.info("Azure DI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Azure DI client: {e}")
    
    def analyze_document(
        self, 
        file_path: str, 
        model_id: str = "prebuilt-layout"
    ) -> Dict[str, Any]:
        """
        分析文件並提取結構化資訊
        
        Args:
            file_path: 文件路徑
            model_id: 使用的模型 ID (預設: prebuilt-layout)
        
        Returns:
            Dict: 包含文字、表格、欄位等結構化資訊
        """
        if not self.client:
            raise ValueError("Azure DI client not initialized")
        
        try:
            logger.info(f"Starting document analysis: {file_path}")
            
            # TODO: 實作實際的文件分析邏輯
            # 這部分需要根據實際 Azure DI API 版本調整
            
            with open(file_path, "rb") as f:
                poller = self.client.begin_analyze_document(
                    model_id=model_id,
                    document=f
                )
            
            result = poller.result()
            
            # 將結果轉換為標準格式
            structured_data = self._convert_to_standard_format(result)
            
            logger.info("Document analysis completed successfully")
            return structured_data
            
        except Exception as e:
            logger.error(f"Document analysis failed: {e}")
            raise
    
    def _convert_to_standard_format(self, result: Any) -> Dict[str, Any]:
        """
        將 Azure DI 結果轉換為標準格式
        
        Args:
            result: Azure DI 分析結果
        
        Returns:
            Dict: 標準化的結構資料
        """
        # TODO: 根據實際需求實作轉換邏輯
        # 此處僅為框架，待實際文件範本後完善
        
        structured_data = {
            "pages": [],
            "tables": [],
            "key_value_pairs": [],
            "raw_text": "",
            "metadata": {}
        }
        
        try:
            # 提取頁面資訊
            if hasattr(result, 'pages'):
                for page in result.pages:
                    page_data = {
                        "page_number": page.page_number if hasattr(page, 'page_number') else 0,
                        "width": page.width if hasattr(page, 'width') else 0,
                        "height": page.height if hasattr(page, 'height') else 0,
                        "lines": [],
                        "words": []
                    }
                    
                    # 提取文字行
                    if hasattr(page, 'lines'):
                        for line in page.lines:
                            page_data["lines"].append({
                                "content": line.content if hasattr(line, 'content') else "",
                                "bounding_box": line.polygon if hasattr(line, 'polygon') else []
                            })
                    
                    structured_data["pages"].append(page_data)
            
            # 提取表格資訊
            if hasattr(result, 'tables'):
                for table in result.tables:
                    table_data = {
                        "row_count": table.row_count if hasattr(table, 'row_count') else 0,
                        "column_count": table.column_count if hasattr(table, 'column_count') else 0,
                        "cells": []
                    }
                    
                    if hasattr(table, 'cells'):
                        for cell in table.cells:
                            table_data["cells"].append({
                                "row_index": cell.row_index if hasattr(cell, 'row_index') else 0,
                                "column_index": cell.column_index if hasattr(cell, 'column_index') else 0,
                                "content": cell.content if hasattr(cell, 'content') else "",
                                "row_span": cell.row_span if hasattr(cell, 'row_span') else 1,
                                "column_span": cell.column_span if hasattr(cell, 'column_span') else 1
                            })
                    
                    structured_data["tables"].append(table_data)
            
            # 提取整體文字內容
            if hasattr(result, 'content'):
                structured_data["raw_text"] = result.content
            
            logger.debug(f"Converted result to standard format: {len(structured_data['pages'])} pages, "
                        f"{len(structured_data['tables'])} tables")
            
        except Exception as e:
            logger.error(f"Error converting result to standard format: {e}")
        
        return structured_data
    
    def extract_tables(self, file_path: str) -> List[Dict[str, Any]]:
        """
        專門提取文件中的表格
        
        Args:
            file_path: 文件路徑
        
        Returns:
            List[Dict]: 表格列表
        """
        result = self.analyze_document(file_path)
        return result.get("tables", [])
    
    def extract_text(self, file_path: str) -> str:
        """
        提取文件中的純文字內容
        
        Args:
            file_path: 文件路徑
        
        Returns:
            str: 文字內容
        """
        result = self.analyze_document(file_path)
        return result.get("raw_text", "")


# 單例模式
_azure_di_service = None

def get_azure_di_service() -> AzureDocumentIntelligenceService:
    """取得 Azure DI 服務實例"""
    global _azure_di_service
    if _azure_di_service is None:
        _azure_di_service = AzureDocumentIntelligenceService()
    return _azure_di_service
