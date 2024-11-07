from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from travel_journals.models import Article, SavedArticle
from travel_journals.filters import ArticleFilter

class ArticleListView(ListView):
    model = Article
    template_name = 'travel_journal/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'travel_journals/article_detail.html'
    context_object_name = 'article'
    def post(self,request, *args, **kwargs):
        article = self.get_object()
        if request.user in article.users_like.all():
            article.users_like.remove(request.user)
        else:
            article.users_like.add(request.user)

        if 'save_article' in request.POST:
            saved_article, created = SavedArticle.objects.get_or_create(
                user=request.user, article=article
            )
            if not created:
                saved_article.delete()

        return redirect(reverse_lazy('travel_journals_app:article_detail', args=[article.pk]))
