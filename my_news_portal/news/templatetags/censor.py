from django import template
import re
#Создаем библиотеку шаблонов(пишем здесь все нежелательные выражения)
register = template.Library()

#Список нежелательных слов
CENSORED_WORDS = [
    'плохое',
    'ужасно',
    'редиска',
    'политика',
    'религия',
    'война'
]
#Регистрируем фильтр с именем 'censor'
@register.filter(name='censor')
def censor_text(value):
#Заменяет нежелательные слова на символы '*'
#Проверяем, что входное значение - строка
    if not isinstance(value, str):
        return value

    text = value
#Перебираем все нежелательные слова
    for word in CENSORED_WORDS:
    #Регулярное выражение для поиска слова, игнорируя регистр
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    #Замена слова на звездочки, сохраняя длину
        replacement = '*' * len(word)
    #Выполняем замену в тексте
        text = pattern.sub(replacement,text)
    return text