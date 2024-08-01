from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet, UserProfileView

urlpatterns = [
    path('register/',UserViewSet.as_view(),name='register'),
    path('profile/',UserProfileView.as_view(),name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
