"""
Date Utilities
日期時間相關的工具函數
"""
from datetime import datetime, timedelta
from typing import Optional


def parse_date_string(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    解析日期字串
    
    Args:
        date_str: 日期字串
        format_str: 日期格式
    
    Returns:
        datetime: 解析後的日期，失敗返回 None
    """
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, TypeError):
        return None


def calculate_days_difference(date1: datetime, date2: datetime) -> int:
    """
    計算兩個日期之間的天數差
    
    Args:
        date1: 日期1
        date2: 日期2
    
    Returns:
        int: 天數差（正數表示 date2 較晚）
    """
    return (date2 - date1).days


def is_within_date_range(
    check_date: datetime,
    start_date: datetime,
    end_date: datetime
) -> bool:
    """
    檢查日期是否在範圍內
    
    Args:
        check_date: 要檢查的日期
        start_date: 開始日期
        end_date: 結束日期
    
    Returns:
        bool: 是否在範圍內
    """
    return start_date <= check_date <= end_date


def format_date_chinese(date: datetime) -> str:
    """
    格式化日期為中文格式
    
    Args:
        date: 日期
    
    Returns:
        str: 中文格式日期 (例如：2026年1月12日)
    """
    return f"{date.year}年{date.month}月{date.day}日"
