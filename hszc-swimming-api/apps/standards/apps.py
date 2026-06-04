"""Standards 应用配置"""
from django.apps import AppConfig


class StandardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.standards'
    verbose_name = '运动员等级标准'