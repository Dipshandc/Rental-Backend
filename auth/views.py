from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import CustomUser,UserProfile
from .serializers import UserCreateSerializer, UserProfileSerializer

class UserViewSet(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Create a new user",
        description="Endpoint to create a new user. Accepts user data and returns a success message.",
        request=UserCreateSerializer,
        responses={
            201: OpenApiExample(
                'User created successfully',
                value={"message": "User created successfully."},
                response_only=True,
            ),
            400: OpenApiExample(
                'Bad Request',
                value={"detail": "Invalid data."},
                response_only=True,
            ),
        },
    )
    def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED, headers=headers)
                
    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        return {}
    
class UserProfileView(APIView):
     serializer_class = UserProfileSerializer
     permission_classes = [IsAuthenticated]
     
     def get(self,request):
          profile = get_object_or_404(UserProfile,user=request.user)
          serializer = self.serializer_class(profile)
          return Response(serializer.data,status=status.HTTP_200_OK)
     
     def patch(self,request):
          profile = get_object_or_404(UserProfile,user=request.user)
          serializer = self.serializer_class(profile,data=request.data,partial=True)
          if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response({"message": f"Profile's {', '.join(request.data.keys())} edited successfully"})
          
