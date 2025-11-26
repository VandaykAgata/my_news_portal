from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    # Копируем QueryDict (все текущие фильтры)
    d = context['request'].GET.copy()
    # Обновляем или добавляем только переданный параметр (например, page=2)
    for k,v in kwargs.items():
        d[k] = v
    #Возвращаем готовую безопасную URL строку
    return d.urlencode()
