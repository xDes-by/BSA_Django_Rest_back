from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from back.views import *
from back import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path("s/", UserListView.as_view()),
    # path("s1/", views.hello_world),
    path("callback/", UserProfileView.as_view()),
    path('login/', views.login),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)