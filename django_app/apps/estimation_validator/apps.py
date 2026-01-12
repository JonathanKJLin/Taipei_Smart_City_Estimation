"""
Estimation Validator App Configuration
"""
from django.apps import AppConfig


class EstimationValidatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.apps.estimation_validator'
    verbose_name = '估驗計價驗證器'
