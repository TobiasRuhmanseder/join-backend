
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from join import views

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/login/', views.LoginView.as_view(), name='api_login_auth'),
    path('api/boards/', views.BoardView.as_view(), name='board_list'),
    path('api/tasks/', views.TaskView.as_view(), name='tasks_list'),
]
