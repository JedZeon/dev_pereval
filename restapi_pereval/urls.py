from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from pereval.views import PassesViewSet
from pereval import urls as doc_url


router = routers.DefaultRouter()
router.register(r'submitData', PassesViewSet, basename='submitData')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(doc_url)),
]

# urlpatterns += doc_url


