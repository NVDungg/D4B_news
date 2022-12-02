from django.shortcuts import render

from django.views.generic import ListView, DetailView, FormView
#use django.views.generic import UpdateView & DeleteView... if don't import forms.py or doens't have
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views import View
from django.views.generic.detail import SingleObjectMixin 

#Mixin  is a special kind of multiple inheritance that Django uses to avoid duplicate code and still allow customization
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Article
from django.urls import reverse_lazy, reverse
from .forms import CommentForm

# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"

class CommentGet(DetailView):
    model = Article
    template_name = "articles/article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class CommentPost(LoginRequiredMixin, SingleObjectMixin, FormView):
    """D4B pages 283
    FormView168 is a built-in view that displays a form, any validation errors, and redirects to a
    new URL. We will use it in combination with SingleObjectMixin169 which helps us associate the
    current article with our form"""
    
    model = Article
    form_class = CommentForm
    template_name = "articles/article_detail.html"

    def post(self, request, *args, **kwargs):
        """grab the article pk from the URL"""
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user    ##set author it instance the one who create commrnt
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})    

class ArticleDetailView(LoginRequiredMixin, View):
    """handle both get/post request. Can use FormView + Detailview but
    this way make a lot of rish and interactions between them
    https://docs.djangoproject.com/en/4.1/topics/class-based-views/mixins/#avoid-anything-more-complex
    So we win separate them"""

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

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

    #set author it the one who create article by form_valid
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
