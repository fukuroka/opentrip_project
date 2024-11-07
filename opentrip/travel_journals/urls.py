from django.urls import path
from travel_journals.views import ArticleListView, ArticleDetailView

app_name = 'travel_journals_app'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),

]
