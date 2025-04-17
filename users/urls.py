from django.urls import path
from . import views
from .views import alumni_list_student



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('terms/', views.terms, name='terms'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('faqs_list/', views.faq_list, name='faq_list'),
    path('ask-question/', views.ask_question, name='ask_question'),
    path('privacy/', views.privacy, name='privacy'),
    path('profile/', views.profile, name='profile'),
    #path('profileinfo/', views.profile_information, name='profileinfo'),
    path('view-profile/', views.profile_view, name='profile_view'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('download/certificate/<int:cert_id>/', views.download_certificate, name='download_certificate'),
    path('delete-certification/<int:cert_id>/', views.delete_certification, name='delete_certification'),
    path('change-password/', views.change_password, name='change_password'),
    
    # urls.py

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('alumni/', alumni_list_student, name='student_alumni'),
    # path('apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),




]