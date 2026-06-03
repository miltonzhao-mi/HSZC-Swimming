"""Notes 序列化器"""
from rest_framework import serializers
from .models import Note, NoteComment, NoteLike


class NoteSerializer(serializers.ModelSerializer):
    """笔记序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    member_avatar = serializers.ImageField(source='member.avatar', read_only=True)

    class Meta:
        model = Note
        fields = [
            'id', 'member', 'member_name', 'member_avatar',
            'title', 'content', 'visibility', 'like_count', 'comment_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'like_count', 'comment_count', 'created_at', 'updated_at']


class NoteCreateSerializer(serializers.ModelSerializer):
    """创建笔记序列化器"""
    class Meta:
        model = Note
        fields = ['title', 'content', 'visibility']


class NoteCommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = NoteComment
        fields = ['id', 'note', 'member', 'member_name', 'content', 'parent', 'replies', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return NoteCommentSerializer(obj.replies.filter(is_deleted=False), many=True).data
        return []


class NoteCommentCreateSerializer(serializers.ModelSerializer):
    """创建评论序列化器"""
    class Meta:
        model = NoteComment
        fields = ['note', 'content', 'parent']


class NoteLikeSerializer(serializers.ModelSerializer):
    """点赞序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)