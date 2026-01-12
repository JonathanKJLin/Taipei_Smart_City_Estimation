"""
Document Processor Serializers
"""
from rest_framework import serializers
from .models import Document, ProcessingLog


class DocumentSerializer(serializers.ModelSerializer):
    """文件序列化器"""
    
    class Meta:
        model = Document
        fields = [
            'id', 'document_id', 'document_type', 'file_name', 
            'file_size', 'status', 'uploaded_at', 'processed_at',
            'confidence_score', 'structured_data', 'validation_result'
        ]
        read_only_fields = ['id', 'document_id', 'uploaded_at', 'processed_at']


class ProcessingLogSerializer(serializers.ModelSerializer):
    """處理日誌序列化器"""
    
    class Meta:
        model = ProcessingLog
        fields = ['id', 'stage', 'message', 'details', 'created_at']
        read_only_fields = ['id', 'created_at']
