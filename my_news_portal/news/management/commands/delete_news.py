from django.core.management import BaseCommand
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        # Добавляем аргумент: имя категории, которую хотим очистить
        parser.add_argument('category',type=str)

    def handle(self, *args, **options):
        category_name = options["category"]

        # 2. Пишем вопрос пользователю в консоль
        self.stdout.write(f'Вы действительно хотите удалить все новости в категории {category_name}? yes/no')

        # 3. Считываем ответ
        answer = input().lower().strip()  # .lower() сделает буквы маленькими, .strip() уберет случайные пробелы

        if answer == 'yes':
            try:
                # Ищем категорию и удаляем связанные новости
                category = Category.objects.get(name=category_name)
                Post.objects.filter(category=category).delete()

                self.stdout.write(self.style.SUCCESS(f'Новости категории {category_name} успешно удалены!'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Категория "{category_name}" не найдена.'))
            return

        # Если ввели не 'yes'
        self.stdout.write(self.style.ERROR('Отказ от удаления'))