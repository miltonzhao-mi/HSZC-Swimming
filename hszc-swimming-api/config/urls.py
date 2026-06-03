"""URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API 路由
    path('api/v1/', include([
        path('users/', include('apps.users.urls')),
        path('members/', include('apps.members.urls')),
        path('competitions/', include('apps.competitions.urls')),
        path('trainings/', include('apps.trainings.urls')),
        path('messages/', include('apps.messages.urls')),
        path('notes/', include('apps.notes.urls')),
    ])),

    # API 文档
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

#