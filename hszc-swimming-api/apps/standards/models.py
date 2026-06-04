"""Standards 模型 - 中国游泳运动员技术等级标准"""
from django.db import models


class SwimmingStandard(models.Model):
    """游泳运动员技术等级标准"""
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    POOL_LENGTH_CHOICES = [
        (50, '50米池'),
        (25, '25米池'),
    ]

    STROKE_CHOICES = [
        ('freestyle', '自由泳'),
        ('backstroke', '仰泳'),
        ('breaststroke', '蛙泳'),
        ('butterfly', '蝶泳'),
        ('medley', '混合泳'),
        ('freestyle_50m', '50米自由泳'),
    ]

    LEVEL_CHOICES = [
        ('international', '国际级运动健将'),
        ('national', '运动健将'),
        ('level_1', '一级运动员'),
        ('level_2', '二级运动员'),
        ('level_3', '三级运动员'),
    ]

    # 核心字段
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES)
    pool_length = models.IntegerField('泳池长度', choices=POOL_LENGTH_CHOICES)
    stroke = models.CharField('泳姿', max_length=20, choices=STROKE_CHOICES)
    distance = models.IntegerField('距离(米)')
    level = models.CharField('等级', max_length=20, choices=LEVEL_CHOICES)

    # 达标成绩（秒）
    qualifying_time = models.DecimalField('达标成绩(秒)', max_digits=8, decimal_places=2)

    # 元数据
    is_active = models.BooleanField('是否启用', default=True)
    version = models.CharField('版本', max_length=20, default='2025')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'standards_swimming'
        verbose_name = '游泳运动员等级标准'
        verbose_name_plural = verbose_name
        ordering = ['gender', 'pool_length', 'stroke', 'distance', 'qualifying_time']
        unique_together = ['gender', 'pool_length', 'stroke', 'distance', 'level']

    def __str__(self):
        level_display = dict(self.LEVEL_CHOICES).get(self.level, self.level)
        stroke_display = dict(self.STROKE_CHOICES).get(self.stroke, self.stroke)
        return f"{dict(self.GENDER_CHOICES).get(self.gender)} {self.pool_length}米池 {stroke_display} {self.distance}米 {level_display} {self.qualifying_time}秒"

    @property
    def level_display(self):
        return dict(self.LEVEL_CHOICES).get(self.level, self.level)

    @property
    def stroke_display(self):
        return dict(self.STROKE_CHOICES).get(self.stroke, self.stroke)

    @property
    def gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, self.gender)

    @property
    def formatted_time(self):
        """格式化成绩为 mm:ss.00"""
        total_seconds = float(self.qualifying_time)
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:05.2f}"