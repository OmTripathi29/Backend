from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .emails import send_otp_via_email,forget_password_email,is_otp_expired
from .serializers import RegisterSerializer, LoginSerializer, verifyEmailSerializer,ResetPasswordSerializer,ForgotPasswordSerializer
from .models import User


@api_view(["POST"])
def register_user(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            send_otp_via_email(serializer.data["email"])
            return Response(
                {
                    "message":"registration successful, check your email for OTP verification",
                    "data":serializer.data,
                    "token":token.key
                },
                status=status.HTTP_201_CREATED
                
            )     
        return Response(
            {"data": serializer.errors,
             "message":"registration failed"},       
            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": serializer.errors}, status=400)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(request, email=email, password=password)
    
    if not user:
        return Response({"error": "Invalid email or password"}, status=401)

    if not user.is_verified:
        return Response({"error": "Email not verified"}, status=403)

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {"message": "Login successful", "token": token.key},
        status=200
    )
@api_view(["POST"])
def verify_otp(request):

    try:
        data = request.data
        serializer = verifyEmailSerializer(data=data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        
        user_queryset = User.objects.filter(email=email)
      
        if not user_queryset.exists():
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
       
        user_instance = user_queryset[0]
        if is_otp_expired(user_instance):
            return Response(
                {"error": "OTP has expired. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_instance.otp_attempts >= 5:
            return Response({"error": "Too many wrong attempts. Request a new OTP."}, status=400)
        
        if user_instance.otp != otp:
            user_instance.otp_attempts += 1
            user_instance.save()
            return Response(
                { 
                    "message": "OTP verification failed.",
                    "data": "Invalid OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
       
        user_instance.is_verified = True
        user_instance.save() 
        
        return Response(
            {"message": "OTP Verified Successfully."},
            status=status.HTTP_200_OK
        )
            
    except Exception as e:
   
        print(f"Error during OTP verification: {e}")
        return Response(
            {"error": "An internal server error occurred.", 
             "detail": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(["POST"])
def reset_password(request):
    try:
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data["email"]
        otp= serializer.validated_data["otp"]
        new_password= serializer.validated_data["new_password"]
        
        user_queryset = User.objects.filter(email=email).first()
        
        if not user_queryset:
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user_queryset.otp != otp:
            return Response(
                {"error": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        if user_queryset.otp_attempts >= 5:
            return Response({"error": "Too many wrong attempts. Request a new OTP."}, status=403) 
        
        user_queryset.set_password(new_password)
        user_queryset.is_verified = True
        user_queryset.otp = None
        user_queryset.otp_created_at = None
        user_queryset.otp_attempts = 0
        user_queryset.save()
        
        return Response(
            {"message": "Password reset successful."},
            status=status.HTTP_200_OK
        )
        
      
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(["POST"])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    email = serializer.validated_data["email"]
    user = User.objects.filter(email=email).first()

    if not user:
        return Response({"error": "User not found"}, status=404)

    forget_password_email(email)
    return Response({"message": "Password reset OTP sent"}, status=200)
