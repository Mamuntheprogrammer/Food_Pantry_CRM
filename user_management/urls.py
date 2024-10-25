from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    # path('password_reset/', views.password_reset, name='password_reset'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logoutview, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),


    path('forgot-password/', views.forgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.passwordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.resetPassword, name='reset-password'),
]
