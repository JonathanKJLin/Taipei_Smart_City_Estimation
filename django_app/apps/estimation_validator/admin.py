"""
Estimation Validator Admin
"""
from django.contrib import admin
from .models import ValidationRule, FeedbackRecord


@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_id', 'rule_name', 'rule_type', 'enabled', 'priority', 'updated_at']
    list_filter = ['rule_type', 'enabled']
    search_fields = ['rule_id', 'rule_name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FeedbackRecord)
class FeedbackRecordAdmin(admin.ModelAdmin):
    list_display = ['document_id', 'field_name', 'feedback_type', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['document_id', 'field_name']
    readonly_fields = ['created_at']
