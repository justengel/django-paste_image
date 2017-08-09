from django.conf.urls import url
from django.contrib import admin

from .views import index

app_name = "test_paste"

urlpatterns = [
    url(r'^(?P<pk>\d+)?$', index, name="index"),
]
