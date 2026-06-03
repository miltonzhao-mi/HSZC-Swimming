"""Users 模型"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """角色表"""
    name = models.CharField('角色名称', max_length=50)
    code = models.CharField('角色代码', max_length=50, unique=True)
    description = models.TextField('描述', blank=True)
    permissions = models.JSONField('权限列表', default=list, blank=True)
    is_system = models.BooleanField('系统角色', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'users_role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """用户表"""
    ROLE_CHOICES = [
        ('global_admin', '全局管理员'),
        ('func_admin', '职能管理员'),
        ('coach', '教练'),
        ('member', '会员'),
    ]

    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='角色'
    )
    phone = models.CharField('手机号', max_length=20, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    user_type = models.CharField('用户类型', max_length=20, choices=ROLE_CHOICES, default='member')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'users_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class OperationLog(models.Model):
    """操作日志"""
    ACTION_CHOICES = [
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
        ('login', '登录'),
        ('logout', '登出'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, verbose_name='操作用户'
    )
    action = models.CharField('操作类型', max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField('模型名称', max_length=100)
    object_id = models.CharField('对象ID', max_length=50, blank=True)
    detail = models.JSONField('详情', default=dict, blank=True)
    ip_address = models.GenericIPAddressField('IP地址', null=True, blank=True)
    user_agent = models.TextField('User-Agent', blank=True)
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        db_table = 'users_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __