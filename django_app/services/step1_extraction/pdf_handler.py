"""
PDF 處理工具
處理 PDF 文件的分割、轉換等操作

從 AZTL 專案重用
"""
import logging
from pathlib import Path
from typing import List, Optional
import PyPDF2
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)


class PDFHandler:
    """PDF 文件處理工具"""
    
    @staticmethod
    def split_pdf(
        input_path: str,
        output_dir: str,
        pages_per_split: Optional[int] = None
    ) -> List[str]:
        """
        分割 PDF 文件
        
        Args:
            input_path: 輸入 PDF 路徑
            output_dir: 輸出目錄
            pages_per_split: 每個分割檔案的頁數 (None 表示每頁一個檔案)
        
        Returns:
            List[str]: 分割後的檔案路徑列表
        """
        try:
            output_paths = []
            
            with open(input_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                logger.info(f"Splitting PDF: {input_path} ({total_pages} pages)")
                
                if pages_per_split is None:
                    pages_per_split = 1
                
                for i in range(0, total_pages, pages_per_split):
                    pdf_writer = PyPDF2.PdfWriter()
                    
                    # 添加頁面
                    end_page = min(i + pages_per_split, total_pages)
                    for page_num in range(i, end_page):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                    
                    # 生成輸出檔案名
                    output_filename = f"split_{i+1}_to_{end_page}.pdf"
                    output_path = Path(output_dir) / output_filename
                    
                    # 寫入檔案
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    
                    output_paths.append(str(output_path))
                    logger.debug(f"Created split file: {output_path}")
            
            logger.info(f"PDF split completed: {len(output_paths)} files created")
            return output_paths
            
        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            raise
    
    @staticmethod
    def pdf_to_images(
        pdf_path: str,
        output_dir: str,
        dpi: int = 300,
        fmt: str = 'PNG'
    ) -> List[str]:
        """
        將 PDF 轉換為圖片
        
        Args:
            pdf_path: PDF 檔案路徑
            output_dir: 輸出目錄
            dpi: 解析度
            fmt: 圖片格式 (PNG, JPEG 等)
        
        Returns:
            List[str]: 圖片檔案路徑列表
        """
        try:
            logger.info(f"Converting PDF to images: {pdf_path}")
            
            # 轉換 PDF 為圖片
            images = convert_from_path(pdf_path, dpi=dpi)
            
            output_paths = []
            output_dir_path = Path(output_dir)
            output_dir_path.mkdir(parents=True, exist_ok=True)
            
            # 儲存圖片
            for i, image in enumerate(images, start=1):
                output_filename = f"page_{i}.{fmt.lower()}"
                output_path = output_dir_path / output_filename
                image.save(output_path, fmt)
                output_paths.append(str(output_path))
                logger.debug(f"Saved image: {output_path}")
            
            logger.info(f"PDF to images conversion completed: {len(output_paths)} images")
            return output_paths
            
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            raise
    
    @staticmethod
    def get_pdf_info(pdf_path: str) -> dict:
        """
        取得 PDF 資訊
        
        Args:
            pdf_path: PDF 檔案路徑
        
        Returns:
            dict: PDF 資訊 (頁數、大小等)
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    "page_count": len(pdf_reader.pages),
                    "file_size": Path(pdf_path).stat().st_size,
                    "metadata": {}
                }
                
                # 提取 metadata
                if pdf_reader.metadata:
                    for key, value in pdf_reader.metadata.items():
                        info["metadata"][key] = value
                
                return info
                
        except Exception as e:
            logger.error(f"Error getting PDF info: {e}")
            raise
    
    @staticmethod
    def merge_pdfs(input_paths: List[str], output_path: str) -> str:
        """
        合併多個 PDF 檔案
        
        Args:
            input_paths: 輸入 PDF 路徑列表
            output_path: 輸出 PDF 路徑
        
        Returns:
            str: 輸出檔案路徑
        """
        try:
            logger.info(f"Merging {len(input_paths)} PDF files")
            
            pdf_writer = PyPDF2.PdfWriter()
            
            for pdf_path in input_paths:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            logger.info(f"PDF merge completed: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            raise
