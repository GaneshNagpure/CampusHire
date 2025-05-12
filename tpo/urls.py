from django.urls import path
from . import views


urlpatterns = [
    path('tpo_dashboard', views.tpo_dashboard, name='tpo_dashboard'),
    path('dashboard/export/', views.export_to_excel, name='export_to_excel'),
    path('tpo_registration/', views.tpo_registration, name='tpo_registration'),
    path('tpo_logout/', views.tpo_logout, name='tpo_logout'),
    path('tpo_account/', views.tpo_update_profile, name='tpo_account'),
    path('', views.tpo_login, name='tpo_login'),
    path('add-job/', views.add_job, name='add-job'),
    path('toggle-job-status/<int:job_id>/', views.toggle_job_status, name='toggle-job-status'),
    path('manage-job/', views.manage_job, name='manage-job'),
    path('update-job/<int:id>/', views.update_job, name='update-job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete-job'),
    path("alumni/add/", views.add_alumni, name="add_alumni"),
    path("alumni/update/<int:alumni_id>/", views.update_alumni, name="update_alumni"),
    path("alumni/toggle/<int:alumni_id>/", views.toggle_alumni_visibility, name="toggle_alumni"),
    path("alumni/list/", views.alumni_list, name="alumni_list"),

    path('applications/', views.tpo_applications_view, name='tpo_applications'),
    path('applications/update_status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    
    path('schedule-drive/', views.schedule_drive, name='schedule-drive'),
    path('manage-drive/', views.manage_drive, name='manage-drive'),
    path('update-drive/<int:drive_id>/', views.update_drive, name='update-drive'),
    path('delete-drive/<int:drive_id>/', views.delete_drive, name='delete-drive'),
    path('drive/update-status/<int:drive_id>/', views.update_drive_status, name='update-drive-status'),

    path('companies/', views.view_companies, name='view_companies'),
    path('companies/add/', views.add_hiring_partner, name='add_hiring_partner'),
    path('companies/update/<int:pk>/', views.update_hiring_partner, name='update_hiring_partner'),
    path('companies/delete/<int:pk>/', views.delete_hiring_partner, name='delete_hiring_partner'),

    path('statics/', views.tpo_dashboard_graphs, name='tpo_graph_dashboard'),

]