"""Notes 应用配置"""
from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notes'
    verbose_name = '笔记社区'
