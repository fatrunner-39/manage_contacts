from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ListUserView, CreateUserView, UserView

router = DefaultRouter()
router.register('registration', CreateUserView)
router.register('users', ListUserView)
router.register('users/<int:pk>/', UserView)


urlpatterns = [
    path('', include(router.urls)),
]
