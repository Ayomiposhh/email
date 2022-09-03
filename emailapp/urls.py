from django.urls import path, include 
from emailapp import views
from django.contrib.auth import views as auth_views

# from second_project import second_app


app_name = 'emailapp'


urlpatterns = [
   
    
    path('register/', views.register, name='register'),
    path('sent/',views.sent, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
   
