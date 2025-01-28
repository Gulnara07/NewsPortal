from django.shortcuts import render
from datetime import datetime

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class News(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'


class Post_Search(ListView):
    model = Post
    ordening = 'date_in'
    template_name = 'flatpages/post_search.html'
    context_object_name = "post_search"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Добавляем новое представление для создания постов.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy('news_articles')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == reverse('news_create'):
            post.post_type = 'NW'
        post.save()
        return super().form_valid(form)


# Добавляем представление для изменения поста.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')
