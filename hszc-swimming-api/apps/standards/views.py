"""Standards 视图"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from decimal import Decimal
from .models import SwimmingStandard
from .serializers import (
    SwimmingStandardSerializer, StandardQuerySerializer, LevelComparisonSerializer
)
from apps.core.response import ApiResponse


class SwimmingStandardViewSet(viewsets.ModelViewSet):
    """游泳等级标准视图集"""
    queryset = SwimmingStandard.objects.filter(is_active=True)
    serializer_class = SwimmingStandardSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['gender', 'pool_length', 'stroke', 'distance', 'level']
    ordering_fields = ['distance', 'qualifying_time']

    @action(detail=False, methods=['get'])
    def levels_by_event(self, request):
        """按项目获取所有等级标准"""
        gender = request.query_params.get('gender')
        pool_length = request.query_params.get('pool_length')
        stroke = request.query_params.get('stroke')
        distance = request.query_params.get('distance')

        queryset = self.get_queryset()

        if gender:
            queryset = queryset.filter(gender=gender)
        if pool_length:
            queryset = queryset.filter(pool_length=int(pool_length))
        if stroke:
            queryset = queryset.filter(stroke=stroke)
        if distance:
            queryset = queryset.filter(distance=int(distance))

        # 按等级排序（从高到低）
        level_order = ['international', 'national', 'level_1', 'level_2', 'level_3']
        queryset = sorted(queryset, key=lambda x: level_order.index(x.level) if x.level in level_order else 99)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=['post'])
    def compare_score(self, request):
        """对比成绩与等级标准"""
        serializer = LevelComparisonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        score_time = Decimal(str(data['score_time']))

        # 查询该项目的所有等级标准
        standards = SwimmingStandard.objects.filter(
            gender=data['gender'],
            pool_length=data['pool_length'],
            stroke=data['stroke'],
            distance=data['distance']
        )

        result = {
            'input_score': float(score_time),
            'input_formatted': self._format_time(score_time),
            'achieved_levels': [],
            'nearest_level': None,
            'next_level': None
        }

        level_order = ['level_3', 'level_2', 'level_1', 'national', 'international']
        level_names = {
            'international': '国际级运动健将',
            'national': '运动健将',
            'level_1': '一级运动员',
            'level_2': '二级运动员',
            'level_3': '三级运动员'
        }

        achieved = []
        next_level_info = None

        for standard in standards:
            if score_time <= standard.qualifying_time:
                achieved.append({
                    'level': standard.level,
                    'level_display': level_names.get(standard.level, standard.level),
                    'qualifying_time': float(standard.qualifying_time),
                    'formatted': self._format_time(standard.qualifying_time)
                })
            else:
                # 找最近的上一级
                if next_level_info is None and standard.level in level_order:
                    idx = level_order.index(standard.level)
                    if idx < len(level_order) - 1:
                        next_level_info = {
                            'level': standard.level,
                            'level_display': level_names.get(standard.level, standard.level),
                            'qualifying_time': float(standard.qualifying_time),
                            'formatted': self._format_time(standard.qualifying_time),
                            'difference': float(score_time - standard.qualifying_time)
                        }

        result['achieved_levels'] = achieved
        result['nearest_level'] = achieved[0] if achieved else None
        result['next_level'] = next_level_info

        return ApiResponse.success(result)

    @action(detail=False, methods=['get'])
    def export_levels(self, request):
        """导出等级标准表格"""
        gender = request.query_params.get('gender')
        pool_length = request.query_params.get('pool_length', 50)

        queryset = self.get_queryset().filter(pool_length=int(pool_length))

        if gender:
            queryset = queryset.filter(gender=gender)

        # 按泳姿和距离分组
        strokes = ['freestyle', 'backstroke', 'breaststroke', 'butterfly', 'medley']
        stroke_names = {
            'freestyle': '自由泳',
            'backstroke': '仰泳',
            'breaststroke': '蛙泳',
            'butterfly': '蝶泳',
            'medley': '混合泳'
        }
        level_order = ['level_3', 'level_2', 'level_1', 'national', 'international']
        level_names = {
            'international': '国际级健将',
            'national': '运动健将',
            'level_1': '一级',
            'level_2': '二级',
            'level_3': '三级'
        }

        result = {}
        for stroke in strokes:
            result[stroke] = {
                'name': stroke_names[stroke],
                'distances': {}
            }
            stroke_qs = queryset.filter(stroke=stroke)
            for dist in [50, 100, 200, 400, 800, 1500]:
                dist_qs = stroke_qs.filter(distance=dist)
                if dist_qs.exists():
                    levels = {}
                    for std in dist_qs:
                        levels[std.level] = {
                            'time': float(std.qualifying_time),
                            'formatted': std.formatted_time
                        }
                    result[stroke]['distances'][dist] = levels

        return ApiResponse.success(result)

    def _format_time(self, seconds):
        """格式化时间"""
        total_seconds = float(seconds)
        minutes = int(total_seconds // 60)
        secs = total_seconds % 60
        return f"{minutes:02d}:{secs:05.2f}"