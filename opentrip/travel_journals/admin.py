from django.contrib import admin
from .models import Category, Tag, Article, ArticleImage, SavedArticle, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'is_public', 'category','total_likes')
    list_filter = ('is_public', 'category', 'tags', 'created_at')
    search_fields = ('title', 'content', 'user__user__username')
    readonly_fields = ('total_likes', )

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'image')
    list_filter = ('article',)
    search_fields = ('article__title',)


@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'saved_at')
    search_fields = ('user__user__username', 'article__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'text', 'created_at')
    search_fields = ('user__user__username', 'article__title', 'text')