from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import ProfileSerializer
from rest_framework import permissions

# Create your views here.
class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            user = User.objects.get(id=user.id)
            user_profile = UserProfile.objects.get(user=user)

            user_profile_serializer = ProfileSerializer(user_profile)
            return Response({'profile': user_profile_serializer.data, 'username': str(username)})
        except:
            return Response({'error': 'Error occurred when trying to get user profile'})

class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            data = self.request.data
            
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            city = data['city']

            user = User.objects.get(id=user.id)
            UserProfile.objects.filter(user=user).update(first_name=first_name, last_name=last_name, phone=phone, city=city)

            user_profile = UserProfile.objects.get(user=user)

            user_profile_serializer = ProfileSerializer(user_profile)
            return Response({'profile': user_profile_serializer.data, 'username': str(username)})
        
        except:
            return Response({'error': 'Something went wrong when trying to update user profile.'})