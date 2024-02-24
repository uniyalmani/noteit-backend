from django.urls import path
from django.urls import path
from auth_app.views import SignUpView, LoginView, RefreshTokenView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
]