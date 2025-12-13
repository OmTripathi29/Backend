from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
from django.utils import timezone
from datetime import timedelta
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_otp_via_email(email):
    
    otp=random.randint(100000, 999999)
    message = Mail(
        from_email=os.environ.get("DEFAULT_FROM_EMAIL", "om@devflowmedia.com"),
        to_email=email,
        subject="Verify Your Email",
        
    )
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.otp_created_at = timezone.now()
    user_obj.otp_attempts = 0 
    user_obj.save()
    try:
        """sg = SendGridAPIClient(os.environ.get("API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)"""
        pass
    except Exception as e:
        print(str(e))
    
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
    
    