import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User, Role, Permission
from datetime import datetime
from api.app_data import *


def populate():

    # Populate superuser role
    permissions = Permission.objects.all()

    try:
        role = Role.objects.get(code_name='su')
        role_permissions = Role.permissions.through.objects.filter(id=role.id)
        role.permissions.clear()
        role_permissions.delete()
    except Role.DoesNotExist:
        role = Role.objects.create(name='SuperUser', code_name='su')

    role.permissions.add(*permissions)
    role.save()

    # Create superuser
    try:
        user = User.objects.get(username='superuser')
    except User.DoesNotExist:
        user = User.objects.create_superuser(
            username="superuser",
            password="password123",
        )
        user.name = 'Superuser'
        user.role = Role.objects.get(code_name='su')
        user.save()


if __name__ == '__main__':
    print("Starting population script...")
    populate()
