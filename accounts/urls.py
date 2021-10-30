from django.urls import path
from django.contrib.auth import views as auth_views

# local imports
from accounts import views as accounts_views
from boards import views

urlpatterns = [
 path("signup/", accounts_views.SignUp, name = "signup"),
 path("login/", auth_views.LoginView.as_view(template_name='../templates/registrations/login.html'), name = "login"),
 path("logout/", auth_views.LogoutView.as_view(), name = "logout"),
 path("password_reset/", accounts_views.PasswordResetRequest, name = "password_reset"),
 path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='../templates/registrations/password_reset_done.html'), name='password_reset_done'),
 path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="../templates/registrations/password_reset_confirm.html"), name='password_reset_confirm'),
 path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='../templates/registrations/password_reset_complete.html'), name='password_reset_complete'), 
 
]
