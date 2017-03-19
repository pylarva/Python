# !/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib.auth.models import Group
from rest_framework import viewsets
from asset.serializers import UserSerializer, GroupSerializer, AssetSerializer, ManufactorySerializer
from asset.user_models import UserProfile
from asset.models import Asset, Manufactory


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AssetViewSet(viewsets.ModelViewSet):
    """
    自定义资产视图
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class ManufactoryViewSet(viewsets.ModelViewSet):
    """
    自定义厂商视图
    """
    queryset = Manufactory.objects.all()
    serializer_class = ManufactorySerializer