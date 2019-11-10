from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signupPage, name='sign up page'),
    path('registration/', views.signupRequest, name='registration'),
    path('login/', views.loginPage, name='login page'),
    path('login-req/', views.loginRequest, name='login request'),
    path('logout/', views.logoutRequest, name='logout request'),
    path('profile/<int:userId>', views.profilePage, name='user profile page')  
]