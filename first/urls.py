from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import users_view, groups_view, update_view, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('savollar/', include('poll.urls', namespace='poll')),
    path('accounts/', include('userprofile.urls', namespace='userprofile')),
    path('news/', include('new.urls', namespace='new')),
    path('groups/', groups_view, name="groups"),
    path('update-user/<int:pk>', update_view, name="user_update"),
    path('users/', users_view, name="users"),
    path('', home, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
