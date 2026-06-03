"""Trainings 模型"""
from django.db import models
from apps.members.models import Member


class TrainingNotice(models.Model):
    """训练通知表"""
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    location = models.CharField('训练地点', max_length=200)
    train_date = models.DateField('训练日期')
    start_time = models.TimeField('开始时间')
    end_time = models.TimeField('结束时间')
    coach = models.CharField('教练', max_length=100)
    max_participants = models.IntegerField('最大人数', null=True, blank=True)
    signup_deadline = models.DateTimeField('报名截止时间')
    notice_type = models.CharField('通知方式', max_length=20,
                                  choices=[('push', '小程序推送'), ('notice', '公告通知')])
    status = models.CharField('状态', max_length=20, default='published',
                            choices=[('draft', '草稿'), ('published', '已发布')])
    created_by = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        null=True, related_name='created_notices',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'trainings_notice'
        verbose_name = '训练通知'
        verbose_name_plural = verbose_name
        ordering = ['-train_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.train_date}"


class TrainingSignUp(models.Model):
    """训练报名表"""
    notice = models.ForeignKey(
        TrainingNotice, on_delete=models.CASCADE,
        related_name='signups',
        verbose_name='训练通知'
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='training_signups',
        verbose_name='会员'
    )
    signup_time = models.DateTimeField('报名时间', auto_now_add=True)
    status = models.CharField('状态', max_length=20, default='registered',
                            choices=[('registered', '已报名'), ('cancelled', '已取消')])

    class Meta:
        db_table = 'trainings_signup'
        verbose_name = '训练报名'
        verbose_name_plural = verbose_name
        unique_together = ['notice', 'member']
        ordering = ['-signup_time']

    def __str__(self):
        return f"{self.member} - {self.notice.title}"


class TrainingNote(models.Model):
    """训练笔记表"""
    VISIBILITY_CHOICES = [
        ('public', '公开'),
        ('private', '私有'),
    ]

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='training_notes',
        verbose_name='会员'
    )
    notice = models.ForeignKey(
        TrainingNotice, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='notes',
        verbose_name='关联训练'
    )
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    visibility = models.CharField('可见性', max_length=20, choices=VISIBILITY_CHOICES, default='public')
    like_count = models.IntegerField('点赞数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'trainings_note'
        verbose_name = '训练笔记'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member} - {self.title}"
