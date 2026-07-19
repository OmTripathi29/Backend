from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
from django.utils import timezone
from datetime import timedelta
import os
from dotenv import load_dotenv
from django.core.mail import send_mail
load_dotenv()



def send_otp_via_email(email):
    otp = random.randint(100000, 999999)

    user = User.objects.get(email=email)
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.otp_attempts = 0
    user.save()

    try:
        send_mail(
            subject="Your OTP for Email Verification",
            message=f"Your OTP is {otp}. It is valid for 10 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        print("Email sent successfully.")

    except Exception as e:
        print("Email sending failed:")
        print(e)
    
def is_otp_expired(user):
    if not user.otp_created_at:
        return True
    expiration_time = user.otp_created_at + timedelta(minutes=10)
    return timezone.now() > expiration_time

def forget_password_email(email):
    otp=random.randint(100000, 999999)
    user_obj=User.objects.get(email=email)
    
    user_obj.otp_created_at = timezone.now()
    try:
        print("Attempting to send OTP email...")
        send_mail(
        subject="Password reset",
        message=f"Your OTP for password reset is: {otp}",
        from_email=os.environ.get("EMAIL_HOST_USER"),
        recipient_list=[email],
        fail_silently=False)
        user_obj.otp=otp
        user_obj.otp_attempts +=1
        return user_obj.save()
    except Exception as e:
        print(str(e))
    user_obj.otp_attempts = 0 
    user_obj.save()
    
    