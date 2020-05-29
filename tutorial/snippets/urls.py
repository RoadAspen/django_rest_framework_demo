from django.urls import include, path
from .views import SnippetViewSet, UserViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
