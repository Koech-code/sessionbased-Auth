from unicodedata import name
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator


# Create your views here.

@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            IsAuthenticated = User.is_authenticated

            if IsAuthenticated:
                return Response({'IsAuthenticated': 'success'})
            else:
                return Response({'error': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication status'})


@method_decorator(csrf_protect, name='dispatch')
class SignUpView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        re_password = data['re_password']

        try:

            if password == re_password:
                if User.objects.filter(username=username).exists():
                    return Response({'error': 'Username already exists'})
                else:
                    if len(password) < 6:
                        return Response({'error': 'Password must be at least 6 characters'})
                    else:
                        user = User.objects.create_user(
                            username=username, password=password)
                        user.save()

                        get_user = User.objects.get(id=user.id)

                        user_profile = UserProfile(
                            user=get_user, first_name='', last_name='', phone='', city='')
                        user_profile.save()

                        return Response({'success': 'User created successfully!'})

            else:
                return Response({'error': 'Passwords do not match'})

        except:
            return Response({'error': 'Something went wrong when registering a user'})


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({'success': 'User authenticates', 'username': username})
            else:
                return Response({'error': 'Error authenticating'})
        except:
            return Response({'error': 'Something went wrong when logging in'})


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'Logged out successfully!'})
        except:
            return Response({'error': 'Something went wrong when logging out'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})


class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user
        try:
            get_user = User.objects.filter(id=user.id).delete()

            return Response({'succes': 'User deleted successfully!'})

        except:
            return Response({'error': 'Something went wrong when trying to delete user'})