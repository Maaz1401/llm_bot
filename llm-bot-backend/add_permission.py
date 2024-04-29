import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'core.settings')

import django
django.setup()

from api.models import Permission

#SHOW AND READ ARE DIFFERENT. SHOW IS USED TO DECIDE WHETHER THE FRONTEND WILL BE VISIBLE TO THE USER. READ IS USED TO DECIDE IF USER WILL BE ABLE TO READ THE DATA.
permissions = [
    Permission(name='Create Role', code_name='role_create', module_name='Role', description='Permission to create role'),
    Permission(name='Read Role', code_name='role_read', module_name='Role', description='Permission to read role'),
    Permission(name='Update Role', code_name='role_update', module_name='Role', description='Permission to update role'),
    Permission(name='Delete Role', code_name='role_delete', module_name='Role', description='Permission to delete role'),
    Permission(name='Show Role', code_name='role_show', module_name='Role', description='Frontend permission to view roles'),

    Permission(name='Create User', code_name='user_create', module_name='User', description='Permission to create user'),
    Permission(name='Read User', code_name='user_read', module_name='User', description='Permission to read user'),
    Permission(name='Update User', code_name='user_update', module_name='User', description='Permission to update user'),
    Permission(name='Delete User', code_name='user_delete', module_name='User', description='Permission to delete user'),
    Permission(name='Show User', code_name='user_show', module_name='User', description='Frontend permission to view users'),
]


def add_permission():
    for permission in permissions:
        try:
            Permission.objects.get(code_name=permission.code_name)
        except Permission.DoesNotExist:
            permission.save()


if __name__ == '__main__':
    print("Adding permissions...")
    add_permission()
