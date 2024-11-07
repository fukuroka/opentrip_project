import django_filters
from django import forms
from travel_journals.models import Article, Category, Tag

class ArticleFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Все категории"
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        label="Теги",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Article
        fields = ['category', 'tags']
