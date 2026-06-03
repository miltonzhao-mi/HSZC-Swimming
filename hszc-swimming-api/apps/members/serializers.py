"""Members 序列化器"""
from rest_framework import serializers
from .models import Member, MemberActivity, MemberLevel


class MemberSerializer(serializers.ModelSerializer):
    """会员序列化器"""
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = Member
        fields = [
            'id', 'user', 'surname', 'given_name', 'full_name',
            'nickname', 'id_card', 'id_card_front', 'id_card_back',
            'avatar', 'gender', 'birth_date', 'age', 'phone',
            'member_type', 'member_status', 'trial_start_date',
            'trial_end_date', 'trial_extended', 'level_points',
            'level_grade', 'approved_by', 'approved_by_name',
            'approved_at', 'approval_remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'level_points']


class MemberCreateSerializer(serializers.ModelSerializer):
    """创建会员序列化器"""

    class Meta:
        model = Member
        fields = [
            'surname', 'given_name', 'nickname', 'id_card',
            'gender', 'birth_date', 'phone'
        ]

    def validate_id_card(self, value):
        if len(value) != 18:
            raise serializers.ValidationError("身份证号格式不正确")
        return value


class MemberApprovalSerializer(serializers.Serializer):
    """会员审批序列化器"""
    approved = serializers.BooleanField()
    remark = serializers.CharField(required=False, allow_blank=True)
    trial_duration = serializers.IntegerField(required=False, min_value=1, max_value=6, default=3)


class MemberActivitySerializer(serializers.ModelSerializer):
    """活跃度记录序列化器"""
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)

    class Meta:
        model = MemberActivity
        fields = [
            'id', 'member', '