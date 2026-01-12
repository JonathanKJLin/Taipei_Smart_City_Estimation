"""
File Utilities
檔案處理相關的工具函數
"""
import os
import hashlib
from pathlib import Path
from typing import Optional
from django.conf import settings


def calculate_file_hash(file_path: str, algorithm: str = 'sha256') -> str:
    """
    計算檔案的 hash 值
    
    Args:
        file_path: 檔案路徑
        algorithm: hash 演算法 (預設: sha256)
    
    Returns:
        str: hash 值
    """
    hash_func = getattr(hashlib, algorithm)()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def get_file_extension(file_path: str) -> str:
    """
    取得檔案副檔名
    
    Args:
        file_path: 檔案路徑
    
    Returns:
        str: 副檔名 (不含 .)
    """
    return Path(file_path).suffix.lstrip('.')


def validate_file_type(file_path: str) -> bool:
    """
    驗證檔案類型是否允許
    
    Args:
        file_path: 檔案路徑
    
    Returns:
        bool: 是否允許
    """
    ext = get_file_extension(file_path).lower()
    allowed_types = settings.ALLOWED_FILE_TYPES
    
    return ext in allowed_types


def validate_file_size(file_path: str, max_size_mb: Optional[int] = None) -> bool:
    """
    驗證檔案大小是否符合限制
    
    Args:
        file_path: 檔案路徑
        max_size_mb: 最大大小(MB)，None 表示使用設定值
    
    Returns:
        bool: 是否符合限制
    """
    if max_size_mb is None:
        max_size_mb = settings.MAX_UPLOAD_SIZE_MB
    
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    
    return file_size_mb <= max_size_mb


def ensure_directory_exists(directory: str):
    """
    確保目錄存在，不存在則建立
    
    Args:
        directory: 目錄路徑
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
