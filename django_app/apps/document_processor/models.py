"""
Document Processor Models
文件處理相關的資料模型
"""
from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    """文件模型"""
    
    DOCUMENT_TYPES = [
        ('estimation', '估驗計價單'),
        ('payment', '付款明細'),
        ('contract', '工程合約'),
        ('other', '其他'),
    ]
    
    STATUS_CHOICES = [
        ('uploaded', '已上傳'),
        ('processing', '處理中'),
        ('completed', '完成'),
        ('failed', '失敗'),
    ]
    
    document_id = models.CharField(max_length=100, unique=True, verbose_name='文件編號')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name='文件類型')
    file_name = models.CharField(max_length=255, verbose_name='檔案名稱')
    file_path = models.CharField(max_length=500, verbose_name='檔案路徑')
    file_size = models.IntegerField(verbose_name='檔案大小(bytes)')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded', verbose_name='處理狀態')
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='上傳者')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上傳時間')
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name='處理完成時間')
    
    # ICR 結果
    icr_result = models.JSONField(null=True, blank=True, verbose_name='ICR結果')
    
    # 結構化資料
    structured_data = models.JSONField(null=True, blank=True, verbose_name='結構化資料')
    
    # 驗算結果
    validation_result = models.JSONField(null=True, blank=True, verbose_name='驗算結果')
    
    # 信心分數
    confidence_score = models.FloatField(null=True, blank=True, verbose_name='信心分數')
    
    # 錯誤訊息
    error_message = models.TextField(null=True, blank=True, verbose_name='錯誤訊息')
    
    class Meta:
        db_table = 'documents'
        verbose_name = '文件'
        verbose_name_plural = '文件'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.document_id} - {self.get_document_type_display()}"


class ProcessingLog(models.Model):
    """處理日誌模型"""
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='logs', verbose_name='文件')
    stage = models.CharField(max_length=50, verbose_name='處理階段')
    message = models.TextField(verbose_name='訊息')
    details = models.JSONField(null=True, blank=True, verbose_name='詳細資訊')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    
    class Meta:
        db_table = 'processing_logs'
        verbose_name = '處理日誌'
        verbose_name_plural = '處理日誌'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document.document_id} - {self.stage}"
