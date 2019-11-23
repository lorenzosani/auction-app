from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('active', views.ActiveAuctionsViewSet)

urlpatterns = [
    path('signup/', views.signupPage, name='sign up page'),
    path('registration/', views.signupRequest, name='registration'),
    path('login/', views.loginPage, name='login page'),
    path('login-req/', views.loginRequest, name='login request'),
    path('logout/', views.logoutRequest, name='logout request'),
    path('profile/<username>', views.profilePage, name='user profile page'),  
    path('forgot/', auth_views.PasswordResetView.as_view(template_name='reset_pw/form.html', success_url='/forgot/sent', html_email_template_name='reset_pw/email.html'), name='forgot password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_pw/confirm.html'), name='password_reset_confirm'),
    path('forgot/sent', views.pwResetSentPage, name='forgot password sent'),
    path('forgot/completed', views.pwResetCompletedPage, name='password_reset_complete'),
    path('sell', views.addNewItem, name='add item'),
    path('item/<item_id>', views.itemDetail, name="item detail"),
    path('item/<item_id>/bid', views.makeBid, name="make bid"),
    path('', views.itemsList, name="items list"),
    path('api/', include(router.urls)),
]