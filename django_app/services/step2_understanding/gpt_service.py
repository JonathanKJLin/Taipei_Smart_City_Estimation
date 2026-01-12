"""
Azure OpenAI GPT Service
處理 GPT-5 相關的自然語言處理任務

從 AZTL 專案重用並修改為 GPT-5
"""
import logging
import json
from typing import Dict, Any, List, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class AzureGPTService:
    """
    Azure OpenAI GPT-5 服務封裝
    提供文件語義理解、欄位對應、邏輯識別等功能
    """
    
    def __init__(self):
        """初始化 Azure OpenAI 客戶端"""
        self.endpoint = settings.AZURE_OPENAI_ENDPOINT
        self.api_key = settings.AZURE_OPENAI_KEY
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME
        self.api_version = settings.AZURE_OPENAI_API_VERSION
        self.client = None
        
        if self.endpoint and self.api_key:
            try:
                from openai import AzureOpenAI
                
                self.client = AzureOpenAI(
                    api_key=self.api_key,
                    api_version=self.api_version,
                    azure_endpoint=self.endpoint
                )
                logger.info(f"Azure OpenAI client initialized successfully (Deployment: {self.deployment_name})")
            except Exception as e:
                logger.error(f"Failed to initialize Azure OpenAI client: {e}")
    
    def process_document(
        self,
        icr_data: Dict[str, Any],
        prompt_template: str,
        response_format: Optional[Dict] = None,
        temperature: float = 0.1,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        使用 GPT-5 處理文件資料
        
        Args:
            icr_data: ICR 擷取的資料
            prompt_template: Prompt 模板
            response_format: 期望的回應格式 (JSON Schema)
            temperature: 溫度參數 (0-1)
            max_tokens: 最大 token 數
        
        Returns:
            Dict: GPT 處理後的結構化資料
        """
        if not self.client:
            raise ValueError("Azure OpenAI client not initialized")
        
        try:
            # 構建完整的 prompt
            full_prompt = self._build_prompt(icr_data, prompt_template)
            
            logger.info(f"Sending request to GPT-5 (deployment: {self.deployment_name})")
            logger.debug(f"Prompt length: {len(full_prompt)} characters")
            
            # 呼叫 GPT-5 API
            messages = [
                {
                    "role": "system",
                    "content": "你是一個專業的文件分析助手，擅長從估驗計價相關文件中提取結構化資訊。"
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
            
            # TODO: 根據實際 GPT-5 API 規格調整參數
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"} if response_format else None
            )
            
            # 解析回應
            result = self._parse_response(response)
            
            logger.info("GPT-5 processing completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"GPT-5 processing failed: {e}")
            raise
    
    def understand_field_mapping(
        self,
        icr_data: Dict[str, Any],
        target_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        理解並對應文件欄位到目標 Schema
        
        Args:
            icr_data: ICR 擷取的資料
            target_schema: 目標資料結構
        
        Returns:
            Dict: 對應後的資料
        """
        # TODO: 實作欄位對應邏輯
        # 載入對應的 prompt 模板
        prompt_template = self._load_prompt_template("field_mapping")
        
        # 加入 schema 資訊到 prompt
        prompt_with_schema = f"{prompt_template}\n\n目標資料結構：\n{json.dumps(target_schema, ensure_ascii=False, indent=2)}"
        
        return self.process_document(
            icr_data=icr_data,
            prompt_template=prompt_with_schema,
            response_format=target_schema
        )
    
    def identify_logic_relationships(
        self,
        structured_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        識別文件中的邏輯關聯
        例如：加總關係、累計關係、條件關係等
        
        Args:
            structured_data: 結構化資料
        
        Returns:
            List[Dict]: 識別出的邏輯關係列表
        """
        # TODO: 實作邏輯關聯識別
        # 此功能在有實際範本後實作
        
        prompt_template = self._load_prompt_template("logic_identification")
        
        result = self.process_document(
            icr_data=structured_data,
            prompt_template=prompt_template
        )
        
        return result.get("logic_relationships", [])
    
    def parse_payment_conditions(
        self,
        condition_text: str
    ) -> Dict[str, Any]:
        """
        解析付款條件描述
        例如：「工程完成30%後支付第二期款」
        
        Args:
            condition_text: 付款條件文字描述
        
        Returns:
            Dict: 結構化的付款條件
        """
        # TODO: 實作付款條件解析
        # 待有實際範本後實作
        
        prompt_template = self._load_prompt_template("payment_condition_parsing")
        
        full_prompt = f"{prompt_template}\n\n付款條件：{condition_text}"
        
        result = self.process_document(
            icr_data={"condition_text": condition_text},
            prompt_template=full_prompt
        )
        
        return result.get("parsed_condition", {})
    
    def _build_prompt(
        self,
        icr_data: Dict[str, Any],
        prompt_template: str
    ) -> str:
        """
        構建完整的 prompt
        
        Args:
            icr_data: ICR 資料
            prompt_template: Prompt 模板
        
        Returns:
            str: 完整的 prompt
        """
        # 將 ICR 資料格式化為文字
        icr_text = json.dumps(icr_data, ensure_ascii=False, indent=2)
        
        # 組合 prompt
        full_prompt = f"{prompt_template}\n\n文件資料：\n{icr_text}"
        
        return full_prompt
    
    def _parse_response(self, response: Any) -> Dict[str, Any]:
        """
        解析 GPT 回應
        
        Args:
            response: GPT API 回應
        
        Returns:
            Dict: 解析後的資料
        """
        try:
            content = response.choices[0].message.content
            
            # 嘗試解析為 JSON
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                logger.warning("Response is not valid JSON, returning as text")
                return {"content": content}
                
        except Exception as e:
            logger.error(f"Error parsing GPT response: {e}")
            return {}
    
    def _load_prompt_template(self, template_name: str) -> str:
        """
        載入 prompt 模板
        
        Args:
            template_name: 模板名稱
        
        Returns:
            str: Prompt 內容
        """
        # TODO: 從檔案系統載入模板
        # 目前返回預設模板
        
        templates = {
            "field_mapping": "請根據提供的文件資料，將欄位對應到目標資料結構。",
            "logic_identification": "請識別文件中的邏輯關聯，包括加總關係、累計關係等。",
            "payment_condition_parsing": "請將付款條件文字描述解析為結構化格式。"
        }
        
        return templates.get(template_name, "請處理以下文件資料。")


# 單例模式
_azure_gpt_service = None

def get_azure_gpt_service() -> AzureGPTService:
    """取得 Azure GPT 服務實例"""
    global _azure_gpt_service
    if _azure_gpt_service is None:
        _azure_gpt_service = AzureGPTService()
    return _azure_gpt_service
