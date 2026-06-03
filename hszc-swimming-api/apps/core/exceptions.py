"""自定义异常"""
from rest_framework.views import exception_handler
from rest_framework import status


class APIException(Exception):
    """基础 API 异常"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = '请求错误'

    def __init__(self, message=None, code=None):
        self.message = message or self.default_message
        self.code = code


class ValidationError(APIException):
    """验证错误"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = '参数校验失败'


class NotFoundError(APIException):
    """资源不存在"""
    status_code = status.HTTP_404_NOT_FOUND
    default_message = '资源不存在'


class UnauthorizedError(APIException):
    """未授权"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = '未授权'


class ForbiddenError(APIException):
    """权限不足"""
    status_code = status.HTTP_403_FORBIDDEN
    default_message = '权限不足'


def custom_exception_handler(exc, context):
    """自定义异常处理"""
    from .response import ApiResponse

    # 调用 REST framework 默认的异常处理
    response = exception_handler(exc, context)

    if isinstance(exc, APIException):
        return ApiResponse.error(
            message=exc.message,
            code=exc.status_code
        )

    if response is not None:
        # 包装默认异常响应
        data = response.data if hasattr(response, 'data') else {}
        message = data.get('detail