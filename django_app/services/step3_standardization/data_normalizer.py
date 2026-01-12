"""
Data Normalizer
資料標準化處理器

將非結構化或半結構化資料轉換為標準格式
"""
import logging
from typing import Dict, Any, List, Union
from decimal import Decimal, InvalidOperation
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class DataNormalizer:
    """
    資料標準化處理器
    負責資料清洗、格式轉換、標準化
    """
    
    def normalize_document(
        self,
        raw_data: Dict[str, Any],
        document_type: str
    ) -> Dict[str, Any]:
        """
        標準化整份文件資料
        
        Args:
            raw_data: 原始資料
            document_type: 文件類型
        
        Returns:
            Dict: 標準化後的資料
        """
        logger.info(f"Normalizing document of type: {document_type}")
        
        try:
            normalized = {
                "document_type": document_type,
                "normalized_at": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            # 標準化基本資訊
            if "document_id" in raw_data:
                normalized["document_id"] = self.normalize_document_id(
                    raw_data["document_id"]
                )
            
            # 標準化合約資訊
            if "contract_info" in raw_data:
                normalized["contract_info"] = self.normalize_contract_info(
                    raw_data["contract_info"]
                )
            
            # 標準化項目明細
            if "items" in raw_data:
                normalized["items"] = self.normalize_items(raw_data["items"])
            
            # 標準化金額
            amount_fields = ["period_amount", "previous_accumulation", "current_accumulation"]
            for field in amount_fields:
                if field in raw_data:
                    normalized[field] = self.normalize_amount(raw_data[field])
            
            # 標準化日期
            if "date" in raw_data:
                normalized["date"] = self.normalize_date(raw_data["date"])
            
            logger.info("Document normalization completed")
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing document: {e}")
            raise
    
    def normalize_document_id(self, doc_id: Any) -> str:
        """
        標準化文件編號
        
        Args:
            doc_id: 原始文件編號
        
        Returns:
            str: 標準化的文件編號
        """
        # 移除多餘空白、統一大寫
        doc_id_str = str(doc_id).strip().upper()
        # 移除特殊字元（保留英數字和連字號）
        doc_id_str = re.sub(r'[^A-Z0-9\-]', '', doc_id_str)
        return doc_id_str
    
    def normalize_amount(self, amount: Any) -> float:
        """
        標準化金額
        
        Args:
            amount: 原始金額（可能是字串、數字等）
        
        Returns:
            float: 標準化的金額
        """
        try:
            # 如果已經是數字
            if isinstance(amount, (int, float, Decimal)):
                return float(amount)
            
            # 如果是字串，移除千分位、貨幣符號等
            if isinstance(amount, str):
                # 移除逗號、貨幣符號、空白
                amount_str = amount.replace(',', '').replace('$', '').replace('NT$', '').replace('元', '').strip()
                # 轉換為數字
                return float(amount_str)
            
            logger.warning(f"Unexpected amount type: {type(amount)}")
            return 0.0
            
        except (ValueError, InvalidOperation) as e:
            logger.error(f"Error normalizing amount '{amount}': {e}")
            return 0.0
    
    def normalize_date(self, date: Any) -> str:
        """
        標準化日期
        
        Args:
            date: 原始日期
        
        Returns:
            str: ISO 格式日期字串 (YYYY-MM-DD)
        """
        try:
            # 如果已經是 datetime
            if isinstance(date, datetime):
                return date.strftime('%Y-%m-%d')
            
            # 如果是字串，嘗試解析
            if isinstance(date, str):
                # 嘗試各種日期格式
                formats = [
                    '%Y-%m-%d',
                    '%Y/%m/%d',
                    '%Y.%m.%d',
                    '%Y年%m月%d日',
                    '%Y%m%d'
                ]
                
                for fmt in formats:
                    try:
                        dt = datetime.strptime(date, fmt)
                        return dt.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
                
                logger.warning(f"Could not parse date: {date}")
                return date
            
            return str(date)
            
        except Exception as e:
            logger.error(f"Error normalizing date '{date}': {e}")
            return str(date)
    
    def normalize_contract_info(
        self,
        contract_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        標準化合約資訊
        
        Args:
            contract_info: 原始合約資訊
        
        Returns:
            Dict: 標準化的合約資訊
        """
        normalized = {}
        
        # 標準化合約編號
        if "contract_number" in contract_info:
            normalized["contract_number"] = self.normalize_document_id(
                contract_info["contract_number"]
            )
        
        # 標準化合約金額
        if "contract_amount" in contract_info:
            normalized["contract_amount"] = self.normalize_amount(
                contract_info["contract_amount"]
            )
        
        # 標準化日期
        for date_field in ["start_date", "end_date"]:
            if date_field in contract_info:
                normalized[date_field] = self.normalize_date(
                    contract_info[date_field]
                )
        
        # 保留其他欄位
        for key, value in contract_info.items():
            if key not in normalized:
                normalized[key] = value
        
        return normalized
    
    def normalize_items(
        self,
        items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        標準化項目明細列表
        
        Args:
            items: 原始項目列表
        
        Returns:
            List[Dict]: 標準化的項目列表
        """
        normalized_items = []
        
        for item in items:
            normalized_item = {}
            
            # 標準化數量和金額欄位
            amount_fields = ["quantity", "unit_price", "amount", 
                           "previous_quantity", "total_quantity"]
            for field in amount_fields:
                if field in item:
                    normalized_item[field] = self.normalize_amount(item[field])
            
            # 保留其他欄位
            for key, value in item.items():
                if key not in normalized_item:
                    normalized_item[key] = value
            
            normalized_items.append(normalized_item)
        
        return normalized_items
    
    def remove_null_values(
        self,
        data: Dict[str, Any],
        recursive: bool = True
    ) -> Dict[str, Any]:
        """
        移除 null 值
        
        Args:
            data: 資料字典
            recursive: 是否遞迴處理
        
        Returns:
            Dict: 清理後的資料
        """
        cleaned = {}
        
        for key, value in data.items():
            if value is None:
                continue
            
            if recursive and isinstance(value, dict):
                cleaned[key] = self.remove_null_values(value, recursive=True)
            elif recursive and isinstance(value, list):
                cleaned[key] = [
                    self.remove_null_values(item, recursive=True) 
                    if isinstance(item, dict) else item
                    for item in value if item is not None
                ]
            else:
                cleaned[key] = value
        
        return cleaned


# 單例模式
_data_normalizer = None

def get_data_normalizer() -> DataNormalizer:
    """取得資料標準化器實例"""
    global _data_normalizer
    if _data_normalizer is None:
        _data_normalizer = DataNormalizer()
    return _data_normalizer
