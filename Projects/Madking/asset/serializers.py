# !/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib.auth.models import Group
from asset.user_models import UserProfile
from rest_framework import serializers
from asset.models import Asset, Manufactory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'name', 'email')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('url', 'id', 'name', 'manufactory')
        depth = 2


class ManufactorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufactory
        fields = ('url', 'manufactory')