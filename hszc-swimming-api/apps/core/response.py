"""统一响应格式"""
from rest_framework.response import Response
from rest_framework import status


class ApiResponse:
    """统一 API 响应"""

    @staticmethod
    def success(data=None, message='success', code=200):
        """成功响应"""
        return Response({
            'code': code,
            'message': message,
            'data': data
        }, status=status.HTTP_200_OK)

    @staticmethod
    def created(data=None, message='创建成功'):
        """创建成功响应"""
        return Response({
            'code': 201,
            'message': message,
            'data': data
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def no_content(message='删除成功'):
        """无内容响应"""
        return Response({
            'code': 204,
            'message': message,
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def error(message='请求错误', code=400, errors=None):
        """错误响应"""
        return Response({
            'code': code,
            'message': message,
            'errors': errors
        }, status=status.HTTP_200_OK)  # 使用 200 避免前端拦截

    @staticmethod
    def unauthorized(message='未授权'):
        """未授权响应"""
        return Response({
            'code': 401,
            'message': message,
        }, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden(message='权限不足'):
        """禁止响应"""
        return Response({
            'code': 403,
            'message': message,
        }, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def not_found(message='资源不存在'):
        """未找到响应"""
        return Response({
            'code': 404,
            'message': message,
        }, status=status.HTTP_200_OK)

    @staticmethod
    def validation_error(errors):
        """验证错误响应"""
        return Response({
            'code': 422,
            'message': '参数校验失败',
            'errors': errors
        }, status=status.HTTP_200_OK)


class SuccessResponse:
    """快捷成功响应"""
    def __init__(self, data=None, message='success'):
        self.data = data
        self.message =