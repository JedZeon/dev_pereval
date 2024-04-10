from django.shortcuts import render
from rest_framework import viewsets

from pereval.models import Passes, Images, Level, Coords, PassUser
from pereval.serializers import PassSerializer, ImagesSerializer, LevelSerializer, CoordsSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = PassUser.objects.all()
    serializer_class = UserSerializer


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PassesViewSet(viewsets.ModelViewSet):
    queryset = Passes.objects.all()
    serializer_class = PassSerializer
