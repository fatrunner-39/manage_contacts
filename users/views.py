from rest_framework import mixins, viewsets, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import MyPermission
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, MyPermission]

    def destroy(self, request, *args, **kwargs):
        user = super().retrieve(request, *args, **kwargs)
        super().destroy(request, *args, **kwargs)
        return Response({"success": f"user with id = {user.data['id']} success deleted"})
