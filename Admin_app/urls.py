from django.urls import path
from .views import home_view, custom_admin_dashboard, register_user, api_stats, login_view
from . import views

urlpatterns = [
    path('', login_view, name='login'),
    path('admin/', custom_admin_dashboard, name='custom_admin_dashboard'),
    path('register/', register_user, name='register'),
    path('api/stats/', api_stats, name='api_stats'),
    path('home/', home_view, name='home_view'),
    path('admin/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('admin/users/', views.users_page, name='users_page'),
    path('admin/authorization/', views.authorization_page, name='authorization_page'),
    path('admin/reports/', views.reports_page, name='reports_page'),
]
