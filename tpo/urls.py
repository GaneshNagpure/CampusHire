from django.urls import path
from . import views


urlpatterns = [
    path('tpo_dashboard', views.tpo_dashboard, name='tpo_dashboard'),
    path('tpo_registration/', views.tpo_registration, name='tpo_registration'),
    path('tpo_logout/', views.tpo_logout, name='tpo_logout'),
    path('tpo_account/', views.tpo_update_profile, name='tpo_account'),
    path('', views.tpo_login, name='tpo_login'),
    path('add-job/', views.add_job, name='add-job'),
    path('manage-job/', views.manage_job, name='manage-job'),
    path('update-job/<int:id>/', views.update_job, name='update-job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete-job'),
    
]