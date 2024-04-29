from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register('roles', views.RoleViewSet, basename='role')
routers.register('roles-unpaginated', views.RoleListViewSet, basename='role')
routers.register('users', views.UserViewSet, basename='user')
routers.register('users-unpaginated', views.UserListViewSet, basename='user')

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('refresh', views.RefreshView.as_view()),
    path('current', views.CurrentUserView.as_view()),
    path('permissions', views.PermissionListView.as_view()),
    path('query-model', views.QueryModelView.as_view()),
    path('last-conversation', views.LastConversationView.as_view()),
]

urlpatterns += routers.urls
