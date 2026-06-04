"""Profiles 视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Q, F, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json

from .models import MemberProfile, PerformanceRecord
from .serializers import (
    MemberProfileSerializer, PerformanceRecordSerializer,
    PerformanceTrendSerializer, ProfileSummarySerializer,
    LeaderboardItemSerializer
)
from apps.core.response import ApiResponse
from apps.standards.models import SwimmingStandard


class MemberProfileViewSet(viewsets.GenericViewSet):
    """会员画像视图集"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from apps.members.models import Member
        return Member.objects.filter(member_status='normal')

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """获取会员画像摘要"""
        member_id = request.query_params.get('member_id')

        if not member_id:
            return ApiResponse.error('缺少member_id参数')

        try:
            member = self.get_queryset().get(id=member_id)
        except:
            return ApiResponse.error('会员不存在')

        # 基础信息
        basic_info = {
            'member_id': member.id,
            'name': member.full_name,
            'gender': member.gender,
            'age': member.age,
            'member_type': member.get_member_type_display(),
            'level_points': member.level_points
        }

        # 计算年龄组
        if member.birth_date:
            today = timezone.now().date()
            age = today.year - member.birth_date.year
            group_start = (age // 5) * 5
            basic_info['age_group'] = f"{group_start}-{group_start+4}岁"
        else:
            basic_info['age_group'] = '-'

        # 获取或创建画像
        profile, _ = MemberProfile.objects.get_or_create(member=member)

        # 成绩统计
        total_events = PerformanceRecord.objects.filter(member=member).count()
        personal_best_count = len(profile.personal_records) if profile.personal_records else 0

        # 活跃度统计
        current_year = timezone.now().year
        year_stats = {
            'signup_count': profile.year_signups,
            'score_count': profile.year_scores,
            'training_count': profile.year_training,
            'points': profile.year_points
        }

        # 总计
        total_stats = {
            'signup_count': profile.total_signups,
            'score_count': profile.total_scores,
            'training_count': profile.total_training,
            'points': profile.total_points
        }

        return ApiResponse.success({
            'basic_info': basic_info,
            'participation_stats': {
                'current_year': year_stats,
                'all_time': total_stats
            },
            'performance_summary': {
                'total_events': total_events,
                'personal_best_count': personal_best_count
            }
        })

    @action(detail=False, methods=['get'])
    def performance_trend(self, request):
        """获取成绩趋势"""
        member_id = request.query_params.get('member_id')
        stroke = request.query_params.get('stroke')
        distance = request.query_params.get('distance', type=int)

        if not member_id:
            return ApiResponse.error('缺少member_id参数')

        queryset = PerformanceRecord.objects.filter(member_id=member_id)

        if stroke:
            queryset = queryset.filter(stroke=stroke)
        if distance:
            queryset = queryset.filter(distance=distance)

        # 按日期排序
        records = queryset.order_by('competition_date')

        if not records.exists():
            return ApiResponse.success({
                'member_id': member_id,
                'event': f"{stroke}{distance}m" if stroke and distance else '全部',
                'data_points': [],
                'trend': 'no_data'
            })

        # 计算趋势
        data_points = []
        previous_time = None
        for record in records:
            current_time = float(record.score_time)
            improvement = None
            if previous_time:
                diff = current_time - previous_time
                if diff < 0:
                    improvement = f"{diff:.2f}秒"
                elif diff > 0:
                    improvement = f"+{diff:.2f}秒"

            total_seconds = current_time
            minutes = int(total_seconds // 60)
            seconds = total_seconds % 60
            formatted_time = f"{minutes:02d}:{seconds:05.2f}"

            data_points.append({
                'date': record.competition_date.strftime('%Y-%m'),
                'time': current_time,
                'formatted_time': formatted_time,
                'rank': record.rank,
                'improvement': improvement,
                'competition_name': record.competition_name
            })
            previous_time = current_time

        # 判断趋势
        if len(data_points) >= 2:
            first_time = data_points[0]['time']
            last_time = data_points[-1]['time']
            improvement_rate = ((first_time - last_time) / first_time) * 100

            if improvement_rate > 5:
                trend = 'improving'
            elif improvement_rate < -5:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
            improvement_rate = 0

        return ApiResponse.success({
            'member_id': member_id,
            'event': f"{stroke}{distance}m" if stroke and distance else '全部',
            'data_points': data_points,
            'trend': trend,
            'improvement_rate': f"{improvement_rate:.1f}%"
        })

    @action(detail=False, methods=['get'])
    def personal_bests(self, request):
        """获取个人最佳成绩"""
        member_id = request.query_params.get('member_id')

        if not member_id:
            return ApiResponse.error('缺少member_id参数')

        # 获取所有该会员的成绩记录
        records = PerformanceRecord.objects.filter(member_id=member_id)

        # 按泳姿和距离分组，取最佳成绩
        best_records = {}
        for record in records:
            key = f"{record.stroke}_{record.distance}"
            if key not in best_records or float(record.score_time) < float(best_records[key].score_time):
                best_records[key] = record

        # 获取会员信息和等级标准
        member = self.get_queryset().filter(id=member_id).first()
        gender = member.gender if member else 'male'
        standards = SwimmingStandard.objects.filter(gender=gender, pool_length=50)

        results = []
        for key, record in best_records.items():
            # 查询该项目的等级标准
            std = standards.filter(stroke=record.stroke, distance=record.distance).first()

            achieved_level = None
            if std and member:
                score = float(record.score_time)
                # 遍历等级，从高到低匹配
                level_order = ['international', 'national', 'level_1', 'level_2', 'level_3']
                for level in level_order:
                    level_std = standards.filter(stroke=record.stroke, distance=record.distance, level=level).first()
                    if level_std and score <= float(level_std.qualifying_time):
                        achieved_level = {
                            'level': level,
                            'level_display': dict(SwimmingStandard.LEVEL_CHOICES).get(level),
                            'qualifying_time': float(level_std.qualifying_time)
                        }
                        break

            total_seconds = float(record.score_time)
            minutes = int(total_seconds // 60)
            seconds = total_seconds % 60

            results.append({
                'stroke': record.stroke,
                'stroke_display': dict(PerformanceRecord._meta.get_field('stroke').choices).get(record.stroke, record.stroke),
                'distance': record.distance,
                'best_time': float(record.score_time),
                'formatted_time': f"{minutes:02d}:{seconds:05.2f}",
                'rank': record.rank,
                'achieved_level': achieved_level,
                'date': record.competition_date.strftime('%Y-%m-%d')
            })

        return ApiResponse.success({
            'member_id': member_id,
            'member_name': member.full_name if member else '-',
            'records': results
        })

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """活跃度排行榜"""
        leader_type = request.query_params.get('type', 'annual')  # annual | all_time
        gender = request.query_params.get('gender')  # male | female
        age_group = request.query_params.get('age_group')  # 30-39
        limit = int(request.query_params.get('limit', 20))

        from apps.members.models import Member
        queryset = Member.objects.filter(member_status='normal')

        if gender:
            queryset = queryset.filter(gender=gender)

        if age_group:
            # 解析年龄组
            try:
                start_age = int(age_group.split('-')[0])
                end_age = int(age_group.split('-')[1].replace('岁', ''))
                current_year = timezone.now().year
                start_birth_year = current_year - end_age
                end_birth_year = current_year - start_age
                queryset = queryset.filter(
                    birth_date__year__gte=start_birth_year,
                    birth_date__year__lte=end_birth_year
                )
            except:
                pass

        # 按积分排序
        if leader_type == 'annual':
            # 年度排行需要通过画像表获取
            queryset = queryset.annotate(
                sort_points=Coalesce('profile__year_points', Value(0))
            ).order_by('-sort_points')
        else:
            queryset = queryset.order_by('-level_points')

        # 获取前N名
        results = []
        for rank, member in enumerate(queryset[:limit], 1):
            profile = getattr(member, 'profile', None)

            results.append({
                'rank': rank,
                'member_id': member.id,
                'member_name': member.full_name,
                'gender': member.gender,
                'age_group': self._calculate_age_group(member.birth_date),
                'level_points': member.level_points,
                'year_points': profile.year_points if profile else 0,
                'total_scores': profile.total_scores if profile else 0,
                'total_signups': profile.total_signups if profile else 0
            })

        return ApiResponse.success({
            'type': leader_type,
            'gender': gender,
            'age_group': age_group,
            'count': len(results),
            'rankings': results
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """会员统计概览"""
        from apps.members.models import Member

        total_members = Member.objects.filter(member_status='normal').count()

        # 性别分布
        gender_stats = Member.objects.filter(
            member_status='normal'
        ).values('gender').annotate(count=Count('id'))

        # 年龄组分布
        today = timezone.now().date()
        age_groups = {}
        for member in Member.objects.filter(member_status='normal'):
            if member.birth_date:
                age = today.year - member.birth_date.year
                group = f"{(age // 5) * 5}-{(age // 5) * 5 + 4}"
                age_groups[group] = age_groups.get(group, 0) + 1

        # 活跃度分布
        point_ranges = [
            ('0-99', 0, 99),
            ('100-299', 100, 299),
            ('300-599', 300, 599),
            ('600+', 600, 99999)
        ]
        points_distribution = {}
        for label, min_p, max_p in point_ranges:
            count = Member.objects.filter(
                member_status='normal',
                level_points__gte=min_p,
                level_points__lte=max_p
            ).count()
            points_distribution[label] = count

        return ApiResponse.success({
            'total_members': total_members,
            'gender_distribution': {g['gender']: g['count'] for g in gender_stats},
            'age_distribution': age_groups,
            'points_distribution': points_distribution
        })

    def _calculate_age_group(self, birth_date):
        """计算年龄组"""
        if birth_date:
            today = timezone.now().date()
            age = today.year - birth_date.year
            group_start = (age // 5) * 5
            return f"{group_start}-{group_start+4}岁"
        return "-"


class PerformanceRecordViewSet(viewsets.ModelViewSet):
    """成绩记录视图集"""
    queryset = PerformanceRecord.objects.all()
    serializer_class = PerformanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['member', 'stroke', 'distance']

    @action(detail=False, methods=['post'])
    def sync_from_scores(self, request):
        """从比赛成绩同步记录"""
        from apps.competitions.models import Score, SignUp

        member_id = request.data.get('member_id')
        if not member_id:
            return ApiResponse.error('缺少member_id参数')

        # 获取该会员的所有成绩
        scores = Score.objects.filter(signup__member_id=member_id)

        synced_count = 0
        for score in scores:
            signup = score.signup
            competition = signup.competition

            record, created = PerformanceRecord.objects.update_or_create(
                member=signup.member,
                stroke=signup.event_item,
                distance=int(signup.distance.replace('m', '')) if isinstance(signup.distance, str) else signup.distance,
                competition_name=competition.name,
                competition_date=competition.start_date,
                defaults={
                    'score_time': score.score_time,
                    'rank': score.rank
                }
            )
            synced_count += 1

        return ApiResponse.success({'synced_count': synced_count}, '同步完成')