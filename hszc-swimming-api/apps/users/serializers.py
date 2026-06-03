"""Users 序列化器"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, OperationLog

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'description', 'permissions', 'is_system', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'avatar',
            'user_type', 'role', 'role_name', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """创建用户序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'phone',
            'user_type', 'role'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField()


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = OperationLog
        fields = [
            'id', 'user', 'username', 'action', 'model_name',
            'object_id', 'detail', 'ip_address', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
