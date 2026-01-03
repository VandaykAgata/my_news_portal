from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post

class Command(BaseCommand):
    help = 'Создает группы пользователей и назначает им права доступа'

    def handle(self, *args, **options):
        # 1. Создаем группы
        authors_group, _ = Group.objects.get_or_create(name='authors')
        common_group, _ = Group.objects.get_or_create(name='common')

        # 2. Получаем тип контента для модели Post
        content_type = ContentType.objects.get_for_model(Post)

        # 3. Список прав, которые мы хотим дать авторам
        permissions_list = [
            'add_post',
            'change_post',
            'view_post',
        ]

        # 4. Находим эти права в базе и добавляем группе authors
        for codename in permissions_list:
            perm = Permission.objects.get(codename=codename, content_type=content_type)
            authors_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Группы и права успешно настроены!'))