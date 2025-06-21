from django.urls import path
from . import views

urlpatterns = [
    path('', views.LawyerListView.as_view(), name='lawyer-list'),
    path('<int:pk>/', views.LawyerDetailView.as_view(), name='lawyer-detail'),
    path('search/', views.lawyer_search, name='lawyer-search'),
    path('stats/', views.specialty_stats, name='specialty-stats'),
]
