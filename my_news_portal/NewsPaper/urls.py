from django.contrib import admin
from django.urls import path, include
from protect.views import IndexView
from django.views.generic import TemplateView
from news.views import openapi_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')), # Для смены языка
    # 1. Обычный сайт(html-страницы)
    path('', include('news.urls')), # Делегируем всё остальное в приложение news
    # 2. Новый API(JSON данные)
    # Теперь по адресу /api/news/ будет отдаваться JSON через DRF
    path('api/', include('news.urls')),

    path('swagger/', TemplateView.as_view(
        template_name='swagger-ui.html',
    ), name='swagger-ui'),

    path('openapi-schema.yml', openapi_schema_view, name='openapi-schema-file'),

    path('protect/', IndexView.as_view(), name='protect'),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),

    # 3. Кнопка Login/Logout для удобства тестирования API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

