"""
Estimation Validator Views
驗證相關的視圖
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ValidationRule, FeedbackRecord
from .serializers import ValidationRuleSerializer, FeedbackRecordSerializer


class ValidationRuleViewSet(viewsets.ModelViewSet):
    """驗證規則視圖集"""
    
    queryset = ValidationRule.objects.all()
    serializer_class = ValidationRuleSerializer
    
    @action(detail=False, methods=['get'])
    def enabled_rules(self, request):
        """取得所有啟用的規則"""
        rules = self.queryset.filter(enabled=True)
        serializer = self.get_serializer(rules, many=True)
        return Response(serializer.data)


class FeedbackRecordViewSet(viewsets.ModelViewSet):
    """回饋記錄視圖集"""
    
    queryset = FeedbackRecord.objects.all()
    serializer_class = FeedbackRecordSerializer
    
    @action(detail=False, methods=['post'])
    def submit_feedback(self, request):
        """提交回饋"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # TODO: 觸發規則學習機制
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
