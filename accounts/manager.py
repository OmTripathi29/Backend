
from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager):
    use_in_migrations=True
    
    def create_user(self, email,mobile, password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not mobile:
            raise ValueError("Mobile number is required")

        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password,**extra_fields):
        user = self.create_user(email=email, mobile=mobile, password=password,**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
