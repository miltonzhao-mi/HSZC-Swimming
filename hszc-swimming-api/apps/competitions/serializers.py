"""Competitions 序列化器"""
from rest_framework import serializers
from .models import Competition, SignUp, Score, ScoreFile, EventItem
from apps.members.serializers import MemberSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    """比赛序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    signup_count = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = [
            'id', 'name', 'description', 'location', 'start_date',
            'end_date', 'sign_up_deadline', 'status', 'poster',
            'created_by', 'created_by_name', 'signup_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_signup_count(self, obj):
        return obj.signups.filter(status='registered').count()


class CompetitionCreateSerializer(serializers.ModelSerializer):
    """创建比赛序列化器"""
    class Meta:
        model = Competition
        fields = [
            'name', 'description', 'location', 'start_date',
            'end_date', 'sign_up_deadline'
        ]


class SignUpSerializer(serializers.ModelSerializer):
    """参赛报名序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    competition_name = serializers.CharField(source='competition.name', read_only=True)

    class Meta:
        model = SignUp
        fields = [
            'id', 'competition', 'competition_name', 'member', 'member_name',
            'event_item', 'distance', 'signup_time', 'register_by', 'status'
        ]
        read_only_fields = ['id', 'signup_time']


class SignUpCreateSerializer(serializers.ModelSerializer):
    """创建报名序列化器"""
    class Meta:
        model = SignUp
        fields = ['competition', 'member', 'event_item', 'distance', 'register_by']


class ScoreSerializer(serializers.ModelSerializer):
    """成绩序列化器"""
    member_name = serializers.CharField(source='signup.member.full_name', read_only=True)
    event_item = serializers.CharField(source='signup.event_item', read_only=True)
    competition_name = serializers.CharField(source='signup.competition.name', read_only=True)
    submit_by_name = serializers.CharField(source='submit_by.username', read_only=True)

    class Meta:
        model = Score
        fields = [
            'id', 'signup', 'member_name', 'event_item', 'competition_name',
            'score_time', 'rank', 'points', 'submit_by', 'submit_by_name',
            'submit_time', 'remarks'
        ]
        read_only_fields = ['id', 'submit_time']


class ScoreCreateSerializer(serializers.ModelSerializer):
    """录入成绩序列化器"""
    class Meta:
        model = Score
        fields = ['signup', 'score_time', 'rank', 'points', 'remarks']


class ScoreFileSerializer(serializers.ModelSerializer):
    """成绩册序列化器"""
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = ScoreFile
        fields = [
            'id', 'competition', 'name', 'file', 'file_type',
            'uploaded_by', 'uploaded_by_name', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_at']


class EventItemSerializer(serializers.ModelSerializer):
    """比赛项目序列化器"""
    class Meta:
        model = EventItem
        fields = ['id', 'name', 'code', 'distances', 'is_active']
