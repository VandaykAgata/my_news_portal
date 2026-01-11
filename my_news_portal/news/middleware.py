import zoneinfo
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone', 'UTC')
        tz = zoneinfo.ZoneInfo(tzname)
        timezone.activate(tz)

        # Определяем тему прямо тут!
        current_hour = timezone.localtime(timezone.now()).hour
        if current_hour >= 18 or current_hour < 6:
            request.theme = 'dark-theme'
        else:
            request.theme = 'light-theme'

        return self.get_response(request)