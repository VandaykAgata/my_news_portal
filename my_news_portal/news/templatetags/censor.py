from django import template

register = template.Library()

# Наш список нежелательных слов (всегда пишем в нижнем регистре) это и есть наш forbidden_words из заданияfrom django import template
CENSORED_WORDS = ['плохое', 'ужасно', 'редиска', 'политика', 'религия', 'война','секс','кровь','сука']


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        return value

    words = value.split()
    result = []

    for word in words:
        # 1. Отделяем знаки препинания (например, от "Редиска,")
        clean_word = word.rstrip('.,!?:;')
        punctuation = word[len(clean_word):]

        # 2. Проверяем слово в нижнем регистре
        if clean_word.lower() in CENSORED_WORDS:
            # 3. Цензурим, сохраняя регистр первой и последней буквы оригинала
            if len(clean_word) > 2:
                # Берем буквы из clean_word (там сохранен оригинальный регистр)
                censored_part = clean_word[0] + "*" * (len(clean_word) - 2) + clean_word[-1]
                result.append(censored_part + punctuation)
            else:
                # Если слово из 2 букв (например, "ад"), просто оставляем как есть
                result.append(word)
        else:
            # Слово не в списке — возвращаем оригинал
            result.append(word)

    return " ".join(result)
