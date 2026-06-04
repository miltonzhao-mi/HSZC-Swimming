"""Profiles 模型"""
from django.db import models
from apps.members.models import Member


class MemberProfile(models.Model):
    """会员画像汇总"""
    member = models.OneToOneField(
        Member, on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='会员'
    )

    # 累计统计
    total_activities = models.IntegerField('累计活动次数', default=0)
    total_signups = models.IntegerField('累计报名次数', default=0)
    total_scores = models.IntegerField('累计有成绩次数', default=0)
    total_training = models.IntegerField('累计参训次数', default=0)
    total_points = models.IntegerField('累计积分', default=0)

    # 年度统计
    year_signups = models.IntegerField('年度报名', default=0)
    year_scores = models.IntegerField('年度有成绩', default=0)
    year_training = models.IntegerField('年度参训', default=0)
    year_points = models.IntegerField('年度积分', default=0)

    # 个人最佳成绩（JSON存储）
    personal_records = models.JSONField('个人最佳成绩', default=dict, blank=True)

    # 更新时间
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'profiles_member_profile'
        verbose_name = '会员画像'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.member} 画像"


class PerformanceRecord(models.Model):
    """成绩历史记录"""
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='performance_records',
        verbose_name='会员'
    )
    stroke = models.CharField('泳姿', max_length=20)
    distance = models.IntegerField('距离(米)')
    score_time = models.DecimalField('成绩(秒)', max_digits=8, decimal_places=2)
    rank = models.IntegerField('名次', null=True, blank=True)
    competition_name = models.CharField('比赛名称', max_length=200)
    competition_date = models.DateField('比赛日期')
    record_date = models.DateTimeField('记录时间', auto_now_add=True)

    class Meta:
        db_table = 'profiles_performance_record'
        verbose_name = '成绩历史'
        verbose_name_plural = verbose_name
        ordering = ['-competition_date']
        indexes = [
            models.Index(fields=['member', 'stroke', 'distance']),
            models.Index(fields=['-competition_date']),
        ]

    def __str__(self):
        return f"{self.member} - {self.stroke}{self.distance}m: {self.score_time}s"