import django_filters as filters
from api.models import User


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    role = filters.CharFilter(field_name='role__name', lookup_expr='icontains')
    role_code = filters.CharFilter(field_name='role__code_name', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['username','role','role_code']
