from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q, Count

import json

from .models import User
from .serializers import UserSerializer

# Serializer requirements
from .models import Woof
from .serializers import WoofSerializer
from rest_framework import generics, mixins, permissions
from rest_framework import viewsets


# testing status response
from rest_framework import status

# Auth API requirements

from django.http import JsonResponse
# Creates a decorated response to the endopoint
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Customized token claims
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Tools fro JWT token authentication
import jwt
from project4.settings import SECRET_KEY
secret = SECRET_KEY

# Import required modules for pagination


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def index(request):
    return render(request, "./build/static/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # first_name = request.POST["first_name"]
        # last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, first_name, last_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Create your views here.


# Token generator api


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)


class WoofListAPIView(generics.ListCreateAPIView):
    # model = Woof

    serializer_class = WoofSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def get_queryset(self):

        return Woof.objects.all()


class FollowingWoofListAPIView(generics.ListCreateAPIView):
    # model = Woof

    serializer_class = WoofSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Decode authorization bearer using jwt library
        authorization = self.request.headers['Authorization']
        token = authorization.split(' ')[1]
        decoded = jwt.decode(token, secret, algorithms=['HS256'])
        user_id = decoded['user_id']
        username = decoded['username']

        # Get information from the following list
        following = User.objects.get(id=user_id).following.all()

        # Get all the woofs from the following users
        woofs = Woof.objects.filter(user__in=following)

        return woofs


class WoofByUsernameListAPIView(generics.ListAPIView):
    serializer_class = WoofSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        This view should return a list of all the woofs for
        the user as determined by the username portion of the URL.
        """
        user = User.objects.get(username=self.kwargs['username'])

        # Return Woof object filtered by User object
        return Woof.objects.filter(user_id=user.id)

# Create an Woof API View to update text information


class WoofUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WoofSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Woof.objects.all()

    def perform_update(self, serializer):
        # Get user information from self object
        requesting_user = self.request.user

        # Print username from Woof object
        woof = Woof.objects.get(id=self.kwargs['pk'])
        woof_user = woof.user.username

        # Check if user is the same as the Woof object
        if requesting_user.username == woof_user:
            # Get serializer info, update the Woof object and set "updated_at" to now time
            serializer.save(updated_at=timezone.now())


class WoofLikeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WoofSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Woof.objects.all()

    def perform_update(self, serializer):
        # Get user information from self object
        requesting_user = self.request

        # Get the liker id
        user_id = requesting_user._auth.payload['user_id']

        # Get woof model
        woof = Woof.objects.get(id=self.kwargs['pk'])

        # Add user ID to woof, so user will like the post
        woof.likes.add(user_id)

        return self


class WoofUnlikeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WoofSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Woof.objects.all()

    def perform_update(self, serializer):
        # Get user information from self object
        requesting_user = self.request

        # Get the liker id
        user_id = requesting_user._auth.payload['user_id']

        # Get woof model
        woof = Woof.objects.get(id=self.kwargs['pk'])

        # Add user ID to woof, so user will like the post
        woof.likes.remove(user_id)

        return self


class UsersListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    # def perform_create(self, serializer):

    #     print(self.request.user)
    #     serializer.save(user=self.request.user)
    #     return self

    # def get_queryset(self):
    #     return Following.objects.all()


class UserFilterListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # Get user info based on username
    def get_queryset(self):

        username = self.kwargs['username']
        return User.objects.filter(username=username)


class UserFollowUpdateApiVIEW(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()

    # Add manytomany relantionship between follower and followee
    def perform_update(self, serializer):
        # Get serialized data
        username = serializer.initial_data['username']
        followee = serializer.initial_data['followee']
        # Query the database for the follower information
        follower = User.objects.get(username=username)

        # Query the database to get the "id" of the "followee"
        followee_id = User.objects.get(username=followee).id

        # Add followee to the follower's following list
        follower.following.add(followee_id)

        return self


class UserUnfollowUpdateApiVIEW(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()

    # Remove manytomany relantionship between follower and followee
    def perform_destroy(self, serializer):

        # Get serialized data
        username = self.request.data['username']
        followee = self.request.data['followee']
        # Query the database for the follower information
        follower = User.objects.get(username=username)

        # Query the database to get the "id" of the "followee"
        followee_id = User.objects.get(username=followee).id

        # Remove the followee from the follower's following list
        follower.following.remove(followee_id)

        return self


class IsFollowingListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'


# Get user info based on username


    def get_queryset(self):

        username = self.kwargs['username']
        follower = User.objects.get(username=username)

        return User.objects.filter(username=username)
