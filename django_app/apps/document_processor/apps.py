"""
Document Processor App Configuration
"""
from django.apps import AppConfig


class DocumentProcessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.apps.document_processor'
    verbose_name = '文件處理器'
