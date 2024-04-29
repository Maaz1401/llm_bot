from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from api.filters import RoleFilter
from api.models import Role
from api.decorator import route_permissions
from api.serializers import RoleSerializer


class RoleListViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer
    queryset = Role.objects.exclude(code_name='su').order_by('id')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RoleFilter

    @route_permissions(['role_read'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
