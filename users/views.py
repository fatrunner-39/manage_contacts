from rest_framework import mixins, viewsets, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class CreateUserView(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = User.objects
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        data.pop('password')
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ListUserView(ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        users = super().list(request, *args, **kwargs)
        return Response([{
            "id": user['id'],
            "username": user['username'],
            "is_admin": user['is_admin']
        } for user in users.data])


class UserView(RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = super().update(request, *args, **kwargs)
        data = user.data
        if data['id'] != request.user.id and not request.user.is_admin:
            return Response(data={'result': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response({
            "id": data['id'],
            "username": data['username'],
            "is_admin": data['is_admin']
        })

