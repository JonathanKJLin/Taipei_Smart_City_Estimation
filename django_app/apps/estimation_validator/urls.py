"""
Estimation Validator URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rules', views.ValidationRuleViewSet, basename='validation-rule')
router.register(r'feedback', views.FeedbackRecordViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
]
