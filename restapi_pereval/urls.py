from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from pereval.views import PassesViewSet


router = routers.DefaultRouter()
router.register(r'submitData', PassesViewSet, basename='submitData')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

