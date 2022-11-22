from django.shortcuts import render

from django.views.generic import ListView, DetailView
#use django.views.generic import UpdateView & DeleteView... if don't import forms.py or doens't have
from django.views.generic.edit import DeleteView, UpdateView, CreateView

#Mixin  is a special kind of multiple inheritance that Django uses to avoid duplicate code and still allow customization
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Article
from django.urls import reverse_lazy
# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"

class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"

class ArticleUpdateView(UserPassesTestMixin ,LoginRequiredMixin, UpdateView):
    model = Article
    fields = ("title", "body")
    template_name = "articles/article_edit.html"

    def test_func(self):
        """Using UserPassesTestMixin override method to check
        if user create this new it's author then it can edit/delete it"""
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "articles/article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(CreateView, LoginRequiredMixin):
    model = Article
    template_name = "articles/article_new.html"
    fields = ("title", "body", )

    #set author it the one who create article
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)