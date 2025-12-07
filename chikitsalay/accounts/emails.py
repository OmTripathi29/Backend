from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
from django.utils import timezone
from datetime import timedelta
import threading

def send_otp_via_email(email):
    subject = "Verify your email"
    otp=random.randint(100000, 999999)
    message = f"Your OTP for email verification is: {otp}"
    email_from = settings.EMAIL_HOST_USER
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.otp_created_at = timezone.now()
    user_obj.otp_attempts = 0 
    user_obj.save()
    threading.Thread(target=send_mail, args=(subject, message, email_from, [email])).start()
    
def is_otp_expired(user):
    if not user.otp_created_at:
        return True
    expiration_time = user.otp_created_at + timedelta(minutes=10)
    return timezone.now() > expiration_time

def forget_password_email(email):
    subject = "Reset your password"
    otp=random.randint(100000, 999999)
    message = f"Your OTP for password reset is: {otp}"
    email_from = settings.EMAIL_HOST_USER
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.otp_created_at = timezone.now()
    user_obj.otp_attempts = 0 
    user_obj.save()
    threading.Thread(target=send_mail, args=(subject, message, email_from, [email])).start()
    