from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from .models import Article
from django.urls import reverse_lazy
# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"
