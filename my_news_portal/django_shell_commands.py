# --- ИМПОРТЫ ---
# Импортируем все необходимое для работы с ORM и моделями
from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment, ARTICLE, NEWS
from django.db.models import Sum


# --- 1. СОЗДАНИЕ ОБЪЕКТОВ (User, Author, Category) ---
print("--- 1. Создание пользователей и базовых объектов ---")
User.objects.all().delete() # Очистка перед запуском
Category.objects.all().delete() # Очистка категорий
#Запускаю очистку так как были неудачные попытки создания

user1 = User.objects.create_user('ivan_author')
user2 = User.objects.create_user('petr_author')
user3 = User.objects.create_user('user_comment')
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

cat1 = Category.objects.create(name='Политика')
cat2 = Category.objects.create(name='Спорт')
cat3 = Category.objects.create(name='Образование')
cat4 = Category.objects.create(name='Наука')

# --- 2. СОЗДАНИЕ ПОСТОВ И КОММЕНТАРИЕВ ---
post1 = Post.objects.create(author=author1, post_type=ARTICLE, title='Влияние ИИ на экономику', text='Текст первой статьи очень длинный, чтобы можно было сделать превью на 124 символа и добавить многоточие в конце.')
post2 = Post.objects.create(author=author1, post_type=ARTICLE, title='Новый метод изучения Python', text='Это вторая статья.')
post3 = Post.objects.create(author=author2, post_type=NEWS, title='Срочная новость о климате', text='Текст новости...')

post1.category.add(cat4)
post2.category.add(cat3, cat4)
post3.category.add(cat1)

comm1 = Comment.objects.create(post=post1, user=user1, text='Отличный комментарий от автора поста.')
comm2 = Comment.objects.create(post=post1, user=user3, text='Интересно, но не согласен.')
comm3 = Comment.objects.create(post=post2, user=user2, text='Полезно для новичков.')
comm4 = Comment.objects.create(post=post3, user=user3, text='Новость вызвала бурное обсуждение.')

# --- 3. КОРРЕКТИРОВКА РЕЙТИНГОВ ---
post1.like(); post1.like() # +2
post2.dislike() # -1
comm1.like() # +1
comm2.dislike() # -1
comm3.like() # +1
comm4.like() # +1

# --- 4. ОБНОВЛЕНИЕ РЕЙТИНГОВ АВТОРОВ ---
author1.update_rating()
author2.update_rating()

# --- 5. ВЫВОД РЕЗУЛЬТАТОВ (По заданию) ---
print("\n--- ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ ПО ЗАДАНИЮ ---")

# А. Лучший пользователь
best_author = Author.objects.all().order_by('-rating').first()
print(f'Лучший автор: {best_author.user.username}, Рейтинг: {best_author.rating}')

# В. Лучшая статья
best_post = Post.objects.all().order_by('-rating').first()
print('\n--- Лучшая статья ---')
print(f'Дата: {best_post.time_in}')
print(f'Автор: {best_post.author.user.username}')
print(f'Рейтинг: {best_post.rating}')
print(f'Заголовок: {best_post.title}')
print(f'Превью: {best_post.preview()}')

# С. Комментарии к этой статье
print('\n--- Комментарии к лучшей статье ---')
comments = Comment.objects.filter(post=best_post).values('user__username', 'rating', 'text')
for comment in comments:
    print(f"Пользователь: {comment['user__username']}, Рейтинг: {comment['rating']}, Текст: {comment['text'][:30]}...")
