from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^asset$', views.AssetView.as_view()),
    url(r'^asset-(?P<b1>\w+)$', views.AssetView.as_view()),
    url(r'^asset-(?P<b1>\w+)-(?P<b2>\w+)$', views.AssetView.as_view()),
    url(r'^asset-(?P<b1>\w+)-(?P<b2>\w+)-(?P<b3>\w+)$', views.AssetView.as_view()),
]