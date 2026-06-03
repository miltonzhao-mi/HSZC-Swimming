"""Users 视图"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Role, OperationLog
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    RoleSerializer, OperationLogSerializer
)
from apps.core.response import ApiResponse

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    """认证视图集"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """登录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                refresh = RefreshToken.for_user(user)

                # 记录登录日志
                OperationLog.objects.create(
                    user=user,
                    action='login',
                    model_name='User',
                    object_id=str(user.id),
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )

                return ApiResponse.success({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }, message='登录成功')
            else:
                return ApiResponse.unauthorized('用户名或密码错误')
        except User.DoesNotExist:
            return ApiResponse.unauthorized('用户名或密码错误')

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """刷新Token"""
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return ApiResponse.error('缺少refresh token')

        try:
            refresh = RefreshToken(refresh_token)
            return ApiResponse.success({
                'access': str(refresh.access_token),
            })
        except Exception:
            return ApiResponse.error('refresh token无效')

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """登出"""
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return ApiResponse.success(message='登出成功')
        except Exception:
            return ApiResponse.success(message='登出成功')

    def get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return ApiResponse.success(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    """角色视图集"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """操作日志视图集"""
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user', 'action', 'model_name']
    ordering_fields = ['-created_at']
