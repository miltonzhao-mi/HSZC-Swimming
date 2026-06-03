"""Competitions 视图"""
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
