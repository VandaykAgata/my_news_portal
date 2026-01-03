from django.core.management.base import BaseCommand
from django.core import serializers
from django.contrib.auth.models import User
from news.models import Post, Category, Author


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Собираем всё в один список для экспорта
        data = (
                list(User.objects.all()) +
                list(Category.objects.all()) +
                list(Author.objects.all()) +
                list(Post.objects.all())
        )

        with open("mydata.json", "w", encoding="utf-8") as f:
            f.write(serializers.serialize("json", data, indent=4, ensure_ascii=False))

        self.stdout.write(self.style.SUCCESS(f"Зацементировано! Сохранено объектов: {len(data)}"))