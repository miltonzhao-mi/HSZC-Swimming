"""Profiles 序列化器"""
from rest_framework import serializers
from .models import MemberProfile, PerformanceRecord
from apps.members.serializers import MemberSerializer
from apps.standards.models import SwimmingStandard


class MemberProfileSerializer(serializers.ModelSerializer):
    """会员画像序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    age = serializers.IntegerField(source='member.age', read_only=True)
    age_group = serializers.SerializerMethodField()
    gender = serializers.CharField(source='member.gender', read_only=True)
    member_type = serializers.CharField(source='member.member_type', read_only=True)

    class Meta:
        model = MemberProfile
        fields = [
            'id', 'member', 'member_name', 'age', 'age_group', 'gender',
            'member_type', 'total_activities', 'total_signups', 'total_scores',
            'total_training', 'total_points', 'year_signups', 'year_scores',
            'year_training', 'year_points', 'personal_records', 'updated_at'
        ]

    def get_age_group(self, obj):
        """计算年龄组"""
        if obj.member and obj.member.birth_date:
            from datetime import date
            today = date.today()
            age = today.year - obj.member.birth_date.year
            group_start = (age // 5) * 5
            return f"{group_start}-{group_start+4}岁"
        return "-"


class PerformanceRecordSerializer(serializers.ModelSerializer):
    """成绩历史序列化器"""
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    formatted_time = serializers.SerializerMethodField()

    class Meta:
        model = PerformanceRecord
        fields = [
            'id', 'member', 'member_name', 'stroke', 'distance',
            'score_time', 'formatted_time', 'rank', 'competition_name',
            'competition_date', 'record_date'
        ]

    def get_formatted_time(self, obj):
        """格式化成绩为 mm:ss.00"""
        total_seconds = float(obj.score_time)
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:05.2f}"


class PerformanceTrendSerializer(serializers.Serializer):
    """成绩趋势序列化器"""
    date = serializers.CharField()
    time = serializers.DecimalField(max_digits=8, decimal_places=2)
    formatted_time = serializers.CharField()
    improvement = serializers.CharField(required=False, allow_null=True)
    rank = serializers.IntegerField(required=False, allow_null=True)


class ProfileSummarySerializer(serializers.Serializer):
    """画像摘要序列化器"""
    member_id = serializers.IntegerField()
    name = serializers.CharField()
    gender = serializers.CharField()
    age_group = serializers.CharField()
    member_type = serializers.CharField()
    level_points = serializers.IntegerField()

    # 成绩统计
    total_events = serializers.IntegerField()
    personal_best_count = serializers.IntegerField()

    # 活跃度
    participation_stats = serializers.DictField()

    # 排名
    rankings = serializers.DictField(required=False)


class LeaderboardItemSerializer(serializers.Serializer):
    """排行榜项"""
    rank = serializers.IntegerField()
    member_id = serializers.IntegerField()
    member_name = serializers.CharField()
    level_points = serializers.IntegerField()
    total_scores = serializers.IntegerField()
    total_signups = serializers.IntegerField()