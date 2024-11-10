from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('branch_dashboard/', views.branch_dashboard, name='branch_dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('file/<int:file_id>/actions/', views.view_file_actions_admin, name='view_file_actions_admin'),
    path('file/<int:file_id>/actions/branch/', views.view_file_actions_branch, name='view_file_actions_branch'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
