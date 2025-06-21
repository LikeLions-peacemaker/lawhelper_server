from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # 헬스 체크
    path('health/', views.health_check, name='health_check'),

    # 회원가입
    path('register/', views.UserRegistrationView.as_view(), name='register'),

    # 로그인
    path('login/', views.custom_login, name='login'),

    # JWT 토큰 갱신
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 사용자 정보
    path('me/', views.user_info, name='user_info'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    # 비밀번호 변경
    path('password/change/', views.PasswordChangeView.as_view(),
         name='password_change'),
]
