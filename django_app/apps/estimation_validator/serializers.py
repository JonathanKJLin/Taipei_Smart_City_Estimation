"""
Estimation Validator Serializers
"""
from rest_framework import serializers
from .models import ValidationRule, FeedbackRecord


class ValidationRuleSerializer(serializers.ModelSerializer):
    """驗證規則序列化器"""
    
    class Meta:
        model = ValidationRule
        fields = '__all__'


class FeedbackRecordSerializer(serializers.ModelSerializer):
    """回饋記錄序列化器"""
    
    class Meta:
        model = FeedbackRecord
        fields = '__all__'
