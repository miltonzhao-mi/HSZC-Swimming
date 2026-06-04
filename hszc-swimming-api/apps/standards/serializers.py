"""Standards 序列化器"""
from rest_framework import serializers
from .models import SwimmingStandard


class SwimmingStandardSerializer(serializers.ModelSerializer):
    """游泳等级标准序列化器"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    stroke_display = serializers.CharField(source='get_stroke_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    formatted_time = serializers.CharField(read_only=True)

    class Meta:
        model = SwimmingStandard
        fields = [
            'id', 'gender', 'gender_display', 'pool_length',
            'stroke', 'stroke_display', 'distance', 'level',
            'level_display', 'qualifying_time', 'formatted_time',
            'is_active', 'version', 'created_at'
        ]


class StandardQuerySerializer(serializers.Serializer):
    """标准查询参数"""
    gender = serializers.ChoiceField(choices=['male', 'female'], required=False)
    pool_length = serializers.IntegerField(required=False)
    stroke = serializers.ChoiceField(
        choices=['freestyle', 'backstroke', 'breaststroke', 'butterfly', 'medley'],
        required=False
    )
    distance = serializers.IntegerField(required=False)
    level = serializers.ChoiceField(
        choices=['international', 'national', 'level_1', 'level_2', 'level_3'],
        required=False
    )


class LevelComparisonSerializer(serializers.Serializer):
    """等级对比查询"""
    gender = serializers.ChoiceField(choices=['male', 'female'])
    pool_length = serializers.IntegerField()
    stroke = serializers.ChoiceField(
        choices=['freestyle', 'backstroke', 'breaststroke', 'butterfly', 'medley']
    )
    distance = serializers.IntegerField()
    score_time = serializers.DecimalField(max_digits=8, decimal_places=2)