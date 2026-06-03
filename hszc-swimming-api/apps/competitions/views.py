"""Competitions 视图"""
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Competition, SignUp, Score, ScoreFile, EventItem
from .serializers import (
    CompetitionSerializer, CompetitionCreateSerializer,
    SignUpSerializer, SignUpCreateSerializer,
    ScoreSerializer, ScoreCreateSerializer,
    ScoreFileSerializer, EventItemSerializer
)
from apps.core.response import ApiResponse


class CompetitionViewSet(viewsets.ModelViewSet):
    """比赛视图集"""
    queryset = Competition.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']
    search_fields = ['name', 'location']
    ordering_fields = ['-start_date', '-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return CompetitionCreateSerializer
        return CompetitionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def sign_up(self, request, pk=None):
        """参赛报名"""
        competition = self.get_object()

        # 检查报名截止时间
        from django.utils import timezone
        if timezone.now() > competition.sign_up_deadline:
            return ApiResponse.error('报名已截止')

        serializer = SignUpCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 检查是否已有报名
        if SignUp.objects.filter(
            competition=competition,
            member=serializer.validated_data['member'],
            event_item=serializer.validated_data['event_item'],
            distance=serializer.validated_data['distance'],
            status='registered'
        ).exists():
            return ApiResponse.error('已报名该项目')

        signup = serializer.save()

        # 记录活跃度
        from apps.members.models import MemberActivity
        MemberActivity.objects.create(
            member=signup.member,
            activity_type='signup',
            activity_date=timezone.now().date(),
            description=f'报名参加{competition.name}'
        )

        return ApiResponse.created(SignUpSerializer(signup).data, '报名成功')

    @action(detail=True, methods=['post'])
    def import_signups(self, request, pk=None):
        """批量导入报名"""
        from utils.excel import ExcelHelper
        file = request.FILES.get('file')
        if not file:
            return ApiResponse.error('请上传文件')

        competition = self.get_object()
        try:
            excel = ExcelHelper(file)
            data = excel.read_data()

            count = 0
            for row in data:
                from apps.members.models import Member
                try:
                    member = Member.objects.get(id_card=row.get('身份证号'))
                    SignUp.objects.get_or_create(
                        competition=competition,
                        member=member,
                        event_item=row.get('参赛项目'),
                        distance=row.get('距离'),
                        defaults={'register_by': 'pc'}
                    )
                    count += 1
                except Member.DoesNotExist:
                    continue

            return ApiResponse.success({'count': count}, '导入成功')
        except Exception as e:
            return ApiResponse.error(f'导入失败: {str(e)}')

    @action(detail=True, methods=['get'])
    def signups(self, request, pk=None):
        """获取报名列表"""
        competition = self.get_object()
        signups = competition.signups.filter(status='registered')
        serializer = SignUpSerializer(signups, many=True)
        return ApiResponse.success(serializer.data)


class SignUpViewSet(viewsets.ModelViewSet):
    """参赛报名视图集"""
    queryset = SignUp.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['competition', 'status', 'register_by']

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpCreateSerializer
        return SignUpSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消报名"""
        signup = self.get_object()
        signup.status = 'cancelled'
        signup.save()
        return ApiResponse.success(message='取消成功')


class ScoreViewSet(viewsets.ModelViewSet):
    """成绩视图集"""
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['signup__competition']

    def get_serializer_class(self):
        if self.action == 'create':
            return ScoreCreateSerializer
        return ScoreSerializer

    def perform_create(self, serializer):
        serializer.save(submit_by=self.request.user)

        # 记录活跃度
        signup = serializer.instance.signup
        from apps.members.models import MemberActivity
        from django.utils import timezone
        MemberActivity.objects.create(
            member=signup.member,
            activity_type='score',
            activity_date=timezone.now().date(),
            description=f'在{signup.competition.name}中获得成绩'
        )

    @action(detail=False, methods=['get'])
    def member_best(self, request):
        """获取会员最佳成绩"""
        member_id = request.query_params.get('member_id')
        event_item = request.query_params.get('event_item')

        if not member_id or not event_item:
            return ApiResponse.error('缺少参数')

        scores = Score.objects.filter(
            signup__member_id=member_id,
            signup__event_item=event_item
        ).order_by('score_time')

        if scores.exists():
            return ApiResponse.success(ScoreSerializer(scores.first()).data)
        return ApiResponse.success(None, '无历史成绩')

    @action(detail=False, methods=['post'])
    def import_scores(self, request):
        """批量导入比赛成绩"""
        from utils.excel import ExcelHelper
        file = request.FILES.get('file')
        competition_id = request.data.get('competition_id')

        if not file:
            return ApiResponse.error('请上传文件')

        try:
            excel = ExcelHelper(file)
            data = excel.read_data()

            success_count = 0
            error_list = []

            for idx, row in enumerate(data, 1):
                try:
                    member_name = row.get('会员姓名', '').strip()
                    event_item = row.get('泳姿', '').strip()
                    distance = row.get('距离', '').strip()
                    score_time = row.get('成绩', None)
                    gender = row.get('性别', '').strip()
                    age_group = row.get('组别', '').strip()
                    rank = row.get('名次', None)
                    points = row.get('积分', 0)
                    activity_name = row.get('活动名称', '').strip()
                    activity_date = row.get('活动日期', None)
                    remarks = row.get('备注', '').strip()

                    if not member_name or not event_item:
                        error_list.append(f'第{idx}行: 会员姓名和泳姿不能为空')
                        continue

                    # 解析成绩（mm:ss.00格式）
                    if score_time:
                        score_seconds = ExcelHelper.parse_time_format(score_time)
                    else:
                        error_list.append(f'第{idx}行: 成绩不能为空')
                        continue

                    # 查找或创建比赛
                    competition = None
                    if competition_id:
                        try:
                            competition = Competition.objects.get(id=competition_id)
                        except Competition.DoesNotExist:
                            pass

                    if not competition and activity_name:
                        # 尝试查找或创建比赛
                        from datetime import date
                        comp_date = date.today()
                        if activity_date:
                            if hasattr(activity_date, 'date'):
                                comp_date = activity_date.date()
                            else:
                                comp_date = activity_date

                        competition, created = Competition.objects.get_or_create(
                            name=activity_name,
                            defaults={
                                'start_date': comp_date,
                                'end_date': comp_date,
                                'sign_up_deadline': datetime.now(),
                                'status': 'finished'
                            }
                        )

                    if not competition:
                        error_list.append(f'第{idx}行: 未指定比赛且无法创建')
                        continue

                    # 查找会员（通过姓名匹配）
                    from apps.members.models import Member
                    member = None
                    # 尝试通过姓名查找（姓 名格式）
                    name_parts = member_name.split()
                    if len(name_parts) >= 2:
                        member = Member.objects.filter(
                            surname=name_parts[0],
                            given_name=name_parts[1] if len(name_parts) > 1 else ''
                        ).first()
                    if not member:
                        # 尝试模糊匹配
                        member = Member.objects.filter(
                            Q(surname__icontains=member_name) | Q(given_name__icontains=member_name)
                        ).first()

                    if not member:
                        error_list.append(f'第{idx}行: 未找到会员 {member_name}')
                        continue

                    # 创建或更新报名
                    signup, _ = SignUp.objects.get_or_create(
                        competition=competition,
                        member=member,
                        event_item=event_item,
                        distance=distance,
                        defaults={'register_by': 'pc'}
                    )

                    # 创建或更新成绩
                    Score.objects.update_or_create(
                        signup=signup,
                        defaults={
                            'score_time': score_seconds,
                            'rank': int(rank) if rank else None,
                            'points': int(points) if points else 0,
                            'submit_by': self.request.user,
                            'remarks': remarks
                        }
                    )

                    success_count += 1

                except Exception as e:
                    error_list.append(f'第{idx}行: {str(e)}')

            return ApiResponse.success({
                'success_count': success_count,
                'error_count': len(error_list),
                'errors': error_list[:20]
            }, '导入完成')

        except Exception as e:
            return ApiResponse.error(f'导入失败: {str(e)}')


class ScoreFileViewSet(viewsets.ModelViewSet):
    """成绩册视图集"""
    queryset = ScoreFile.objects.all()
    serializer_class = ScoreFileSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['competition']


class EventItemViewSet(viewsets.ModelViewSet):
    """比赛项目视图集"""
    queryset = EventItem.objects.filter(is_active=True)
    serializer_class = EventItemSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def distances(self, request):
        """获取所有距离配置"""
        items = EventItem.objects.filter(is_active=True)
        result = {}
        for item in items:
            result[item.code] = item.distances
        return ApiResponse.success(result)
