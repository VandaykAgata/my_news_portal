from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# --- Константы для выбора типа поста ---
ARTICLE = 'AR'
NEWS = 'NW'
TYPE_CHOICES = [
    (ARTICLE, 'Статья'),
    (NEWS, 'Новость')
]
# --- 1. Модель Author ---
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        from django.db.models import Sum

        posts_rating = self.post_set.aggregate(pr=Sum('rating')).get('pr', 0) * 3
        author_comments_rating = self.user.comment_set.aggregate(acr=Sum('rating')).get('acr', 0)
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Sum('rating')).get('pcr', 0)

        self.rating = posts_rating + author_comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return self.user.username
# --- 2. Модель Category ---
class Category(models.Model):
    # Название категории. Должно быть уникальным.
    name = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return self.name
# --- 3. Модель Post ---
class Post(models.Model):
    # Связь «один ко многим» с Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Поле с выбором — «статья» или «новость»
    post_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=ARTICLE)
    #Автоматически добавляемая дата и время создания
    time_in = models.DateTimeField(auto_now_add=True)
    #Связь "многие ко многим" с Category через PostCategory
    category = models.ManyToManyField(Category, through='PostCategory')
    #Заголовок
    title = models.CharField(max_length=255)
    #Текст
    text = models.TextField()
    #Рейтинг
    rating = models.IntegerField(default=0)
    def like(self):
        self.rating +=1
        self.save()
    def dislike(self):
        self.rating -=1
        self.save()
    def preview(self):
        return f'{self.text[:124]}...'
    def __str__(self):
        return f'{self.title} ({self.author.user.username})'
    def get_absolute_url(self):
        return reverse ('post_detail', args=[str(self.id)])
# --- 4. Модель PostCategory (Промежуточная таблица) ---
class PostCategory(models.Model):
    # Связь "один ко многим" с Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Связь «один ко многим» с Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
# --- 5. Модель Comment ---
class Comment(models.Model):
    # Связь «один ко многим» с Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Связь «один ко многим» со встроенной моделью User (комментатор)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Текст комментария
    text = models.TextField()
    # Дата и время создания комментария
    time_in = models.DateTimeField(auto_now_add=True)
    # Рейтинг комментария
    rating = models.IntegerField(default=0)
    def like(self):
        self.rating +=1
        self.save()
    def dislike(self):
        self.rating -=1
    def __str__(self):
        return f'{self.user.username}:{self.text[:50]}...'
class Article(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    pub_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title



