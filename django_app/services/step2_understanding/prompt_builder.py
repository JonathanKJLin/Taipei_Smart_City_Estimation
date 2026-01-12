"""
Prompt Builder
Prompt 構建器

負責根據不同場景構建 GPT Prompt
"""
import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Prompt 構建器
    根據不同的任務類型構建適當的 Prompt
    """
    
    def __init__(self, templates_dir: str = None):
        """
        初始化 Prompt Builder
        
        Args:
            templates_dir: Prompt 模板目錄路徑
        """
        if templates_dir is None:
            # 預設使用專案中的模板目錄
            current_dir = Path(__file__).parent.parent
            self.templates_dir = current_dir / "templates" / "prompt"
        else:
            self.templates_dir = Path(templates_dir)
        
        logger.info(f"Prompt Builder initialized with templates: {self.templates_dir}")
    
    def build_extraction_prompt(
        self,
        icr_data: Dict[str, Any],
        document_type: str = "estimation"
    ) -> str:
        """
        構建資料擷取 Prompt
        
        Args:
            icr_data: ICR 掃描結果
            document_type: 文件類型
        
        Returns:
            str: 完整的 Prompt
        """
        template = self._load_template("field_extraction.txt")
        
        # 根據文件類型調整 Prompt
        type_instructions = self._get_type_specific_instructions(document_type)
        
        prompt = f"""
{template}

【文件類型】: {document_type}
【特殊說明】: {type_instructions}

【ICR 掃描結果】:
{self._format_icr_data(icr_data)}

請根據以上資訊，提取所有相關欄位並以 JSON 格式輸出。
"""
        return prompt
    
    def build_logic_identification_prompt(
        self,
        structured_data: Dict[str, Any]
    ) -> str:
        """
        構建邏輯識別 Prompt
        
        Args:
            structured_data: 結構化資料
        
        Returns:
            str: 完整的 Prompt
        """
        template = self._load_template("logic_identification.txt")
        
        prompt = f"""
{template}

【結構化資料】:
{self._format_json(structured_data)}

請識別出所有的邏輯關聯關係，並以 JSON 格式輸出。
"""
        return prompt
    
    def build_condition_parsing_prompt(
        self,
        condition_text: str,
        context: Dict[str, Any] = None
    ) -> str:
        """
        構建付款條件解析 Prompt
        
        Args:
            condition_text: 付款條件文字
            context: 上下文資訊
        
        Returns:
            str: 完整的 Prompt
        """
        template = self._load_template("payment_condition_parsing.txt")
        
        context_str = ""
        if context:
            context_str = f"\n【上下文資訊】:\n{self._format_json(context)}"
        
        prompt = f"""
{template}

【付款條件文字】: {condition_text}
{context_str}

請將付款條件解析為結構化格式，並以 JSON 輸出。
"""
        return prompt
    
    def build_few_shot_prompt(
        self,
        base_prompt: str,
        examples: List[Dict[str, Any]]
    ) -> str:
        """
        構建 Few-shot Learning Prompt
        
        Args:
            base_prompt: 基礎 Prompt
            examples: 範例列表 (input-output pairs)
        
        Returns:
            str: 包含範例的 Prompt
        """
        examples_str = "\n\n".join([
            f"【範例 {i+1}】\n輸入：{ex['input']}\n輸出：{ex['output']}"
            for i, ex in enumerate(examples)
        ])
        
        prompt = f"""
{base_prompt}

以下是一些範例供參考：

{examples_str}

現在請處理實際資料：
"""
        return prompt
    
    def _load_template(self, template_name: str) -> str:
        """
        載入 Prompt 模板
        
        Args:
            template_name: 模板檔案名稱
        
        Returns:
            str: 模板內容
        """
        try:
            template_path = self.templates_dir / template_name
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load template {template_name}: {e}")
            return f"# Template {template_name} 載入失敗"
    
    def _get_type_specific_instructions(self, document_type: str) -> str:
        """
        取得文件類型特定的指示
        
        Args:
            document_type: 文件類型
        
        Returns:
            str: 特定指示
        """
        instructions = {
            "estimation": "注意區分「本期」與「累計」數值，確保所有金額欄位為數值型態",
            "payment": "重點關注付款條件、付款期數、付款比例等資訊",
            "contract": "提取合約編號、合約金額、期限等關鍵資訊"
        }
        return instructions.get(document_type, "請仔細提取所有欄位")
    
    def _format_icr_data(self, icr_data: Dict[str, Any]) -> str:
        """格式化 ICR 資料以便閱讀"""
        import json
        return json.dumps(icr_data, ensure_ascii=False, indent=2)
    
    def _format_json(self, data: Dict[str, Any]) -> str:
        """格式化 JSON 資料"""
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)


# 單例模式
_prompt_builder = None

def get_prompt_builder() -> PromptBuilder:
    """取得 Prompt Builder 實例"""
    global _prompt_builder
    if _prompt_builder is None:
        _prompt_builder = PromptBuilder()
    return _prompt_builder
