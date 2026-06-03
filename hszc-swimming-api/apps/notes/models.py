"""Notes 模型"""
from django.db import models
from apps.members.models import Member


class Note(models.Model):
    """笔记表"""
    VISIBILITY_CHOICES = [
        ('public', '公开'),
        ('private', '私有'),
    ]

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='会员'
    )
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    visibility = models.CharField('可见性', max_length=20, choices=VISIBILITY_CHOICES, default='public')
    like_count = models.IntegerField('点赞数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'notes_note'
        verbose_name = '笔记'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member} - {self.title}"


class NoteComment(models.Model):
    """笔记评论表"""
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='笔记'
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='note_comments',
        verbose_name='评论人'
    )
    content = models.TextField('评论内容')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='replies',
        verbose_name='父评论'
    )
    is_deleted = models.BooleanField('已删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'notes_note_comment'
        verbose_name = '笔记评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    def __str__(self):
        return f"{self.member} on {self.note.title}"


class NoteLike(models.Model):
    """笔记点赞表"""
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='笔记'
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='note_likes',
        verbose_name='点赞人'
    )
    created_at = models.DateTimeField('点赞时间', auto_now_add=True)

    class Meta:
        db_table = 'notes_note_like'
        verbose_name = '笔记点赞'
        verbose_name_plural = verbose_name
        unique_together = ['note', 'member']

    def __str__(self):
        return f"{self.member} liked {self.note.title}"
