from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin,\
    RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import Value as V
from rest_framework.response import Response

from .models import Contact
from .serializers import ContactSerializer


class ListContactView(ListModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['lastname', 'firstname', 'secondname', 'company', 'post', 'email', 'phone']
    ordering_fields = ['lastname', 'firstname', 'secondname', 'company', 'post', 'email', 'phone']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        query = request.query_params.get('fullname')
        if query:
            queryset = queryset.annotate(full_name=Concat('lastname', V(' '), 'firstname', V(' '), 'lastname')). \
                filter(full_name__icontains=query)
        else:
            queryset = queryset

        if request.user.is_admin or request.user.id == 1:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(deleted=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateContactView(CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['creator_id'] = request.user.id
        return super().create(request, *args, **kwargs)


class UpdateDeleteContactView(UpdateModelMixin,
                              DestroyModelMixin,
                              RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = Contact.objects
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id != instance.creator_id_id and (not request.user.is_admin) and request.user.id != 1:
            return Response(data={"error": f"Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        contact_id = instance.id
        if request.user.id != instance.creator_id_id and (not request.user.is_admin) and request.user.id != 1:
            return Response(data={"error": f"Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        instance.deleted = True
        instance.save()
        return Response(data={"success": f"Contact with id={contact_id} deleted"})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if (not request.user.is_admin) and instance.deleted:
            return Response(data={"error": f"Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
