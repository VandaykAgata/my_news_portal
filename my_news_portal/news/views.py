#from django.shortcuts import render
#from django.template.context_processors import request

from .models import Article
from django.views.generic import ListView,DetailView




class ArticleListView(ListView):
    model=Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    ordering = ['-pub_date']

class ArticleDetailView(DetailView):
    model=Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'