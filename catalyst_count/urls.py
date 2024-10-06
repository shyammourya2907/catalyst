from django.contrib import admin
from django.urls import path, include
# from user import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('excel/', include('excel_upload.urls')),
    path('', include('user.urls')),
    # path('accounts/', include('allauth.urls')),
    # path('', views.home_view, name='home'),
    # path('accounts/profile/', views.profile, name='account_profile'),
    # path('accounts/signup/', views.custom_signup_view, name='account_signup'),
    # path('accounts/login/', views.custom_login_view, name='account_login'),
    # path('accounts/logout/', views.custom_logout_view, name='account_logout'),
    # path('accounts/password/reset/', views.custom_forget_password_view, name='account_reset_password'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# admin@gmail.com
# Auth@123
