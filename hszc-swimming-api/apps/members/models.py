"""Members 模型"""
from django.db import models
from django.conf import settings


class Member(models.Model):
    """会员表"""
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    MEMBER_TYPE_CHOICES = [
        ('temp', '临时会员'),
        ('formal', '正式会员'),
        ('active', '活跃会员'),
    ]

    MEMBER_STATUS_CHOICES = [
        ('normal', '正常'),
        ('disabled', '禁用'),
        ('cancelled', '已注销'),
    ]

    # 基本信息
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='member_profile',
        null=True, blank=True,
        verbose_name='关联用户'
    )
    surname = models.CharField('姓', max_length=50)
    given_name = models.CharField('名', max_length=50)
    nickname = models.CharField('昵称', max_length=100, blank=True)

    # 证件信息
    id_card = models.CharField('身份证号', max_length=18, unique=True)
    id_card_front = models.ImageField('身份证正面', upload_to='id_cards/', null=True, blank=True)
    id_card_back = models.ImageField('身份证背面', upload_to='id_cards/', null=True, blank=True)
    avatar = models.ImageField('免冠照片', upload_to='avatars/', null=True, blank=True)

    # 个人信息
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField('出生日期')
    phone = models.CharField('联系电话', max_length=20)

    # 会员状态
    member_type = models.CharField('会员类型', max_length=20, choices=MEMBER_TYPE_CHOICES, default='temp')
    member_status = models.CharField('会员状态', max_length=20, choices=MEMBER_STATUS_CHOICES, default='normal')

    # 考核期信息
    trial_start_date = models.DateField('考核开始日期', null=True, blank=True)
    trial_end_date = models.DateField('考核结束日期', null=True, blank=True)
    trial_extended = models.BooleanField('是否延期', default=False)

    # 活跃度信息
    level_points = models.IntegerField('活跃度积分', default=0)
    level_grade = models.CharField('等级', max_length=50, blank=True)

    # 审核信息
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_members',
        verbose_name='审批人'
    )
    approved_at = models.DateTimeField('审批时间', null=True, blank=True)
    approval_remark = models.TextField('审批备注', blank=True)

    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'members_member'
        verbose_name = '会员'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.surname}{self.given_name}({self.nickname})"

    @property
    def full_name(self):
        return f"{self.surname}{self.given_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class MemberActivity(models.Model):
    """会员活跃度记录"""
    ACTIVITY_TYPE_CHOICES = [
        ('signup', '参赛报名'),
        ('score', '比赛有成绩'),
        ('relay', '参与接力'),
        ('training_signup', '训练报名'),
        ('note_publish', '发布训练心得'),
        ('note_like', '心得被点赞'),
        ('note_comment', '心得被评论'),
    ]

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='会员'
    )
    activity_type = models.CharField('活动类型', max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    activity_date = models.DateField('活动日期')
    description = models.CharField('描述', max_length=200, blank=True)
    points = models.IntegerField('积分', default=1)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'members_activity'
        verbose_name = '活跃度记录'
        verbose_name_plural = verbose_name
        ordering = ['-activity_date', '-created_at']

    def __str__(self):
        return f"{self.member} - {self.get_activity_type_display()}"


class MemberLevel(models.Model):
    """会员等级表"""
    name = models.CharField('等级名称', max_length=50)
    code = models.CharField('等级代码', max_length=50, unique=True)
    min_points = models.IntegerField('最低积分')
    max_points = models.IntegerField('最高积分', null=True, blank=True)
    description = models.TextField('描述', blank=True)
    sort_order = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'members_level'
        verbose_name = '会员等级'
        verbose_name_plural = verbose_name
        ordering = ['min_points']

    def __str__(self):
        return self.name
