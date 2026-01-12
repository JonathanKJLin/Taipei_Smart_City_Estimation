"""
Estimation Validator Models
驗證相關的資料模型
"""
from django.db import models


class ValidationRule(models.Model):
    """驗證規則模型"""
    
    RULE_TYPES = [
        ('amount', '金額驗算'),
        ('accumulation', '累計檢核'),
        ('payment', '付款條件'),
        ('custom', '自訂規則'),
    ]
    
    rule_id = models.CharField(max_length=100, unique=True, verbose_name='規則 ID')
    rule_name = models.CharField(max_length=200, verbose_name='規則名稱')
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES, verbose_name='規則類型')
    description = models.TextField(verbose_name='規則描述')
    
    enabled = models.BooleanField(default=True, verbose_name='是否啟用')
    priority = models.IntegerField(default=0, verbose_name='優先級')
    
    rule_config = models.JSONField(null=True, blank=True, verbose_name='規則配置')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    
    class Meta:
        db_table = 'validation_rules'
        verbose_name = '驗證規則'
        verbose_name_plural = '驗證規則'
        ordering = ['-priority', 'rule_id']
    
    def __str__(self):
        return f"{self.rule_id} - {self.rule_name}"


class FeedbackRecord(models.Model):
    """回饋記錄模型"""
    
    FEEDBACK_TYPES = [
        ('correct', '正確'),
        ('incorrect', '錯誤'),
        ('partial', '部分正確'),
    ]
    
    document_id = models.CharField(max_length=100, verbose_name='文件編號')
    field_name = models.CharField(max_length=100, verbose_name='欄位名稱')
    
    system_value = models.JSONField(verbose_name='系統值')
    correct_value = models.JSONField(verbose_name='正確值')
    
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, verbose_name='回饋類型')
    comment = models.TextField(null=True, blank=True, verbose_name='備註')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    
    class Meta:
        db_table = 'feedback_records'
        verbose_name = '回饋記錄'
        verbose_name_plural = '回饋記錄'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document_id} - {self.field_name}"
