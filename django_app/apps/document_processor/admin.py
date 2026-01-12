"""
Document Processor Admin
"""
from django.contrib import admin
from .models import Document, ProcessingLog


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['document_id', 'document_type', 'file_name', 'status', 'confidence_score', 'uploaded_at']
    list_filter = ['document_type', 'status', 'uploaded_at']
    search_fields = ['document_id', 'file_name']
    readonly_fields = ['uploaded_at', 'processed_at']


@admin.register(ProcessingLog)
class ProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['document', 'stage', 'message', 'created_at']
    list_filter = ['stage', 'created_at']
    search_fields = ['document__document_id', 'message']
    readonly_fields = ['created_at']
