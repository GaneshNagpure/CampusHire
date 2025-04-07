from django.urls import path
from . import views


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


]