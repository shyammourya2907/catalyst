
from django.urls import path
from user import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/profile/', views.profile, name='account_profile'),
    path('accounts/signup/', views.custom_signup_view, name='account_signup'),
    path('accounts/login/', views.custom_login_view, name='account_login'),
    path('accounts/logout/', views.custom_logout_view, name='account_logout'),
    # path('accounts/password/reset/', views.custom_forget_password_view, name='account_reset_password'),
]
