from django.urls import path
from .views import register_user, login_user,verify_otp,forgot_password,reset_password

urlpatterns = [
    
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("verifyotp/",verify_otp, name="verifyotp "),
    path("forgot_password/",forgot_password, name="forgot_password "),
    path("reset_password/",reset_password, name="reset_password "),
]

