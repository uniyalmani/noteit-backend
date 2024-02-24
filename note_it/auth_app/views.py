from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import CustomUser
from django.contrib.auth import authenticate
from .serializers.user_serializers import CustomUserSerializer, UserLoginSerializer
from .utils import error_response, success_response


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return success_response({
                    'refresh': str(refresh),
                    'access': str(access_token),
                }, message="Account creation successful", status_code=status.HTTP_201_CREATED)
            else:
                # Check for unique constraints and provide appropriate error messages
                email_errors = serializer.errors.get('email', [])
                name_errors = serializer.errors.get('name', [])
                errors = {}
                fileds = ""
                if email_errors:
                    errors['email'] = 'A user with this email already exists.'
                    fileds += " email, "
                if   name_errors:
                    errors['name'] = 'A user with this name already exists.'
                    fileds += " name "
                
                message = 'A user with' + fileds + "already exists."
                if errors:
                    return error_response(errors=errors, message=message, status_code=status.HTTP_400_BAD_REQUEST)
                else:
                    # Return generic error message for other validation errors
                    return error_response(errors=serializer.errors, message="validation error check formate of email and other fields", status_code=status.HTTP_400_BAD_REQUEST)
               
        except Exception as e:
            # Log the exception for debugging
            print(e)
            return error_response(message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            
            if serializer.is_valid(raise_exception=True):
                email = serializer.data.get("email")
                password = serializer.data.get("password")
                user = authenticate(email=email, password=password)
                
                if user:
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    return success_response(data={
                        'refresh': str(refresh),
                        'access': str(access_token),
                    }, message='Login successful', status_code=status.HTTP_200_OK)
                else:
                    return error_response({'error': 'Invalid credentials'}, message="Invalid email or password. Please check your credentials.", status_code=status.HTTP_401_UNAUTHORIZED)
        except serializers.ValidationError as e:
            # Handle validation errors from serializer
            return error_response(errors=e.detail, message="Validation error", status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other exceptions
            return error_response(errors=str(e), message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class RefreshTokenView(APIView):

    permission_classes = [permissions.AllowAny]

    
    def post(self, request, *args, **kwargs):
        try:
            # Retrieve the refresh token from the request data
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return error_response(errors='Invalid refresh token', status_code=status.HTTP_400_BAD_REQUEST)

            RefreshToken.algorithms = ["HS256"]
            refresh = RefreshToken(refresh_token, verify=True)
            access_token = str(refresh.access_token)
            
            return success_response(data={'access_token': access_token, 
                                          'refresh_token': refresh_token},
                                    message='Token refreshed successfully', 
                                    status_code=status.HTTP_200_OK)

        except TokenError as e:
            return error_response(errors='Invalid refresh token', status_code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return error_response(errors=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)