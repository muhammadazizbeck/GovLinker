from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('password-change/',views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change-done/',views.PasswordChangeDoneView.as_view(),name='password_change_done'),
]