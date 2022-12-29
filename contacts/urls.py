from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreateContactView, ListContactView, UpdateDeleteContactView

router = DefaultRouter()
router.register('contacts/create', CreateContactView)
router.register('contacts', ListContactView)
router.register('contacts', UpdateDeleteContactView)


urlpatterns = [
    path('', include(router.urls)),
]
