from django.contrib import admin
from django.urls import path, include
from protect.views import IndexView


urlpatterns = [
    path('', include('news.urls')),
    path('admin/', admin.site.urls),
    path('protect/', IndexView.as_view(), name='protect'),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
]