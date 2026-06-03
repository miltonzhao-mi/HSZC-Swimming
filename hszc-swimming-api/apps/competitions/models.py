"""Competitions 模型"""
from django.db import models
from apps.members.models import Member


class Competition(models.Model):
    """比赛表"""
    STATUS_CHOICES = [
        ('preparing', '筹备中'),
        ('registration', '报名中'),
        ('ongoing', '进行中'),
        ('finished', '已结束'),
    ]

    name = models.CharField('比赛名称', max_length=200)
    description = models.TextField('描述', blank=True)
    location = models.CharField('地点', max_length=200)
    start_date = models.DateField('开始日期')
    end_date = models.DateField('结束日期')
    sign_up_deadline = models.DateTimeField('报名截止时间')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='preparing')
    poster = models.ImageField('海报', upload_to='competition_posters/', null=True, blank=True)
    created_by = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        null=True, related_name='created_competitions',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'competitions_competition'
        verbose_name = '比赛'
        verbose_name_plural = verbose_name
        ordering = ['-start_date']

    def __str__(self):
        return self.name


class SignUp(models.Model):
    """参赛报名表"""
    REGISTER_BY_CHOICES = [
        ('miniapp', '小程序'),
        ('pc', 'PC端'),
    ]

    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE,
        related_name='signups',
        verbose_name='比赛'
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='signups',
        verbose_name='会员'
    )
    event_item = models.CharField('参赛项目', max_length=50)
    distance = models.CharField('距离', max_length=20)
    signup_time = models.DateTimeField('报名时间', auto_now_add=True)
    register_by = models.CharField('报名渠道', max_length=20, choices=REGISTER_BY_CHOICES)
    status = models.CharField('状态', max_length=20, default='registered',
                            choices=[('registered', '已报名'), ('cancelled', '已取消')])

    class Meta:
        db_table = 'competitions_signup'
        verbose_name = '参赛报名'
        verbose_name_plural = verbose_name
        unique_together = ['competition', 'member', 'event_item', 'distance']
        ordering = ['-signup_time']

    def __str__(self):
        return f"{self.member} - {self.competition.name} - {self.event_item}"


class Score(models.Model):
    """比赛成绩表"""
    signup = models.OneToOneField(
        SignUp, on_delete=models.CASCADE,
        related_name='score',
        verbose_name='报名'
    )
    score_time = models.DecimalField('比赛成绩(秒)', max_digits=8, decimal_places=2)
    rank = models.IntegerField('名次', null=True, blank=True)
    points = models.IntegerField('积分', default=0)
    submit_by = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        null=True, related_name='submitted_scores',
        verbose_name='提交人'
    )
    submit_time = models.DateTimeField('提交时间', auto_now_add=True)
    remarks = models.TextField('备注', blank=True)

    class Meta:
        db_table = 'competitions_score'
        verbose_name = '比赛成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.signup.member} - {self.signup.event_item}: {self.score_time}s"


class ScoreFile(models.Model):
    """比赛成绩册"""
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE,
        related_name='score_files',
        verbose_name='比赛'
    )
    name = models.CharField('文件名称', max_length=200)
    file = models.FileField('文件', upload_to='score_files/')
    file_type = models.CharField('文件类型', max_length=20, default='pdf')
    uploaded_by = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        null=True, related_name='uploaded_score_files',
        verbose_name='上传人'
    )
    uploaded_at = models.DateTimeField('上传时间', auto_now_add=True)

    class Meta:
        db_table = 'competitions_score_file'
        verbose_name = '成绩册'
        verbose_name_plural = verbose_name
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.competition.name} - {self.name}"


class EventItem(models.Model):
    """比赛项目配置"""
    name = models.CharField('项目名称', max_length=50, unique=True)
    code = models.CharField('项目代码', max_length=50, unique=True)
    distances = models.JSONField('距离列表', default=list)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 'competitions_event_item'
        verbose_name = '比赛项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
