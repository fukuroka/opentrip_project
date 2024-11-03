from django.db import models
from django.conf import settings




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_public = models.BooleanField(default=True, verbose_name='Публичный')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True, verbose_name='Теги')
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True, verbose_name='Лайки')
    saved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through="SavedArticle", verbose_name='Сохранено пользователями')


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.users_like.count()



class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_images', verbose_name='Статья')
    image = models.ImageField(upload_to='article_images/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение статьи'
        verbose_name_plural = 'Изображения статьи'

    def __str__(self):
        return f"Image for {self.article.title}"


class SavedArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="saved_articles")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Статья", related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата сохранения")

    class Meta:
        verbose_name = "Сохраненная статья"
        verbose_name_plural = "Сохраненные статьи"
        unique_together = ("user", "article")

    def __str__(self):
        return f"{self.article.title} saved by {self.user.username}"



class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_comments', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.article.title}"