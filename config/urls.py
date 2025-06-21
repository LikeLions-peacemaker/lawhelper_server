from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Chat app URL include
    path('chat/', include('apps.chat.urls')),
    
    # Lawyers app URL include
    path('lawyers/', include('apps.lawyers.urls')),

    # Authentication APIs
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/social/', include('dj_rest_auth.registration.urls')),

    # Custom APIs
    path('api/accounts/', include('apps.accounts.urls')),
]

# 미디어 파일 서빙 (개발 환경에서만)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
