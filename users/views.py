from rest_framework import mixins, viewsets, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = super().retrieve(request, *args, **kwargs)
        data = user.data
        if data['id'] != request.user.id and not request.user.is_admin and request.user.id != 1:
            return Response(data={'result': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response(data)

    def update(self, request, *args, **kwargs):
        user = super().update(request, *args, **kwargs)
        data = user.data
        if data['id'] != request.user.id and not request.user.is_admin and request.user.id != 1:
            return Response(data={'result': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        user = super().retrieve(request, *args, **kwargs)
        data = user.data
        super().destroy(request, *args, **kwargs)
        if data['id'] != request.user.id and not request.user.is_admin and request.user.id != 1:
            return Response(data={'result': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response({"success": f"user with id = {user.data['id']} success deleted"})
