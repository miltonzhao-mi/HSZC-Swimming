"""Members 视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Member, MemberActivity, MemberLevel
from .serializers import (
    MemberSerializer, MemberCreateSerializer, MemberApprovalSerializer,
    MemberActivitySerializer, MemberLevelSerializer
)
from apps.core.response import ApiResponse
from apps.core.pagination import MyPageNumberPagination


class MemberViewSet(viewsets.ModelViewSet):
    """会员视图集"""
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination
    filterset_fields = ['member_type', 'member_status', 'gender']
    search_fields = ['surname', 'given_name', 'nickname', 'phone', 'id_card']
    ordering_fields = ['-created_at', '-level_points']

    def get_serializer_class(self):
        if self.action == 'create':
            return MemberCreateSerializer
        return MemberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        # 创建关联的系统用户
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = f"member_{member.id}_{member.phone}"
        user = User.objects.create_user(
            username=username,
            phone=member.phone,
            user_type='member'
        )
        member.user = user
        member.save()

        return ApiResponse.created(MemberSerializer(member).data)

    @action(detail=False, methods=['post'])
    def import_excel(self, request):
        """Excel批量导入会员"""
        from utils.excel import ExcelHelper
        file = request.FILES.get('file')
        if not file:
            return ApiResponse.error('请上传文件')

        try:
            excel = ExcelHelper(file)
            data = excel.read_data()

            members = []
            for row in data:
                member = Member(
                    surname=row.get('姓', ''),
                    given_name=row.get('名', ''),
                    nickname=row.get('昵称', ''),
                    id_card=row.get('身份证号', ''),
                    gender=row.get('性别', 'male'),
                    birth_date=row.get('出生日期'),
                    phone=row.get('联系电话', ''),
                )
                members.append(member)

            Member.objects.bulk_create(members, ignore_conflicts=True)
            return ApiResponse.success({'count': len(members)}, '导入成功')
        except Exception as e:
            return ApiResponse.error(f'导入失败: {str(e)}')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """审批会员"""
        member = self.get_object()
        serializer = MemberApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        approved = serializer.validated_data['approved']
        remark = serializer.validated_data.get('remark', '')
        trial_duration = serializer.validated_data.get('trial_duration', 3)

        if approved:
            member.member_type = 'temp'
            member.trial_start_date = timezone.now().date()
            member.trial_end_date = timezone.now().date() + timedelta(days=trial_duration * 30)
            member.approval_remark = remark
            member.save()
            return ApiResponse.success(MemberSerializer(member).data, '审批通过')
        else:
            member.member_status = 'disabled'
            member.approval_remark = remark
            member.save()
            return ApiResponse.success(MemberSerializer(member).data, '审批未通过')

    @action(detail=True, methods=['post'])
    def upgrade(self, request, pk=None):
        """升级会员"""
        member = self.get_object()
        member_type = request.data.get('member_type', 'formal')

        if member_type == 'formal':
            member.member_type = 'formal'
        elif member_type == 'active':
            member.member_type = 'active'

        member.save()
        return ApiResponse.success(MemberSerializer(member).data, '升级成功')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """注销会员"""
        member = self.get_object()
        member.member_status = 'cancelled'
        member.save()
        return ApiResponse.success(message='注销成功')

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """会员统计"""
        total = Member.objects.count()
        temp = Member.objects.filter(member_type='temp').count()
        formal = Member.objects.filter(member_type='formal').count()
        active = Member.objects.filter(member_type='active').count()
        cancelled = Member.objects.filter(member_status='cancelled').count()

        return ApiResponse.success({
            'total': total,
            'temp': temp,
            'formal': formal,
            'active': active,
            'cancelled': cancelled,
        })


class MemberActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """会员活跃度视图集"""
    queryset = MemberActivity.objects.all()
    serializer_class = MemberActivitySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['member', 'activity_type']

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """活跃度排行榜"""
        year = request.query_params.get('year', timezone.now().year)
        gender = request.query_params.get('gender')

        members = Member.objects.filter(
            member_status='normal'
        ).annotate(
            year_points=sum('activities__points')
        ).order_by('-level_points')[:20]

        serializer = MemberSerializer(members, many=True)
        return ApiResponse.success(serializer.data)
