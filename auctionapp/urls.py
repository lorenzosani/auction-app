from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signupPage, name='sign up page'),
    path('registration/', views.signupRequest, name='registration')
]