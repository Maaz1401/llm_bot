import imp
from django.contrib import admin
from api.models.user import User
from api.models.role import Role
from api.models.permission import Permission
from api.models.log import Log
from api.models.document import Document
from api.models.message import Message
from api.models.session import Session


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields ]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Role._meta.fields ]

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Permission._meta.fields ]

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Log._meta.fields ]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Document._meta.fields ]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.fields ]

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Session._meta.fields ]