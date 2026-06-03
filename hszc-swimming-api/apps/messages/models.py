"""Messages 模型"""
from django.db import models


class Message(models.Model):
    """消息表"""
    TYPE_CHOICES = [
        ('competition', '比赛通知'),
        ('training', '训练通知'),
        ('system', '系统通知'),
        ('announcement', '公告'),
    ]

    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    message_type = models.CharField('消息类型', max_length=20, choices=TYPE_CHOICES)
    sender = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        null=True, related_name='sent_messages',
        verbose_name='发送人'
    )
    is_published = models.BooleanField('是否发布', default=False)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'messages_message'
        verbose_name = '消息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.get_message_type_display()}]"


class MessageRead(models.Model):
    """消息阅读记录表"""
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE,
        related_name='read_records',
        verbose_name='消息'
    )
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        related_name='message_reads',
        verbose_name='用户'
    )
    is_read = models.BooleanField('已读', default=False)
    read_at = models.DateTimeField('阅读时间', null=True, blank=True)

    class Meta:
        db_table = 'messages_read'
        verbose_name = '消息阅读