from django.contrib import admin
from django.urls import path, include  # <-- Убедись, что 'include' здесь!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
]