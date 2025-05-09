"""
URL configuration for web_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls.static import static
from django.conf import settings
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', staff_member_required(admin.site.urls), name='admin'),
    path('logouts/', user_views.logout, name='logout_confirm'),
    path('register/', user_views.register, name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', user_views.verify_email, name='verify-email'),
    path('profile/', user_views.profile, name='profile'),
    path('<int:user_id>/follow/', user_views.follow_user, name='follow_user'),
    path('<int:user_id>/unfollow/', user_views.unfollow_user, name='unfollow_user'),
    path('<int:user_id>/friend-request/', user_views.send_friend_request, name='send_friend_request'),
    path('<int:user_id>/accept-request/', user_views.accept_friend_request, name='accept_friend_request'),
    path('user/<str:username>/', user_views.user_profile, name='user_profile'),
    path('user_list/', user_views.UserListView.as_view(), name="user_list"),
    path('user_list/<int:user_id>/', user_views.UserDetailView, name="user_detail"),
    path('story/', user_views.story_create, name='story_create'),
    path('story/<int:pk>/', user_views.Storydetails.as_view(), name="story_details"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html',email_template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('', include('YMC.urls')),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
