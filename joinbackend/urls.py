
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from join import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'task_category', views.TaskCategoryViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'boards', views.BoardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', views.LoginView.as_view(), name='api_login_auth'),
    path('api/signup/', views.UserCreateView.as_view(), name='user_create'),
]
