from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import viewsets, permissions
from .filters import PostFilter
from .forms import PostForm
from django.views.decorators.cache import cache_page # импортируем декоратор для кэширования отдельного представления
from django.core.cache import cache # импортируем наш кэш
from django.utils.translation import gettext as _ # импортируем функцию для перевода
from .serializers import *
from .models import *
import pytz #  импортируем стандартный модуль для работы с часовыми поясами

class News(ListView):
    model = Post
    ordering = ['-date_in']
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка постов

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список постов
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'
    queryset = Post.objects.all()


    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


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
    #success_url = reverse_lazy('news_create')


    def form_valid(self, form):
        post = form.save(commit=False)
        #post.author = Author.objects.get_or_create(user=self.request.user)[0]
        post.author = Author.objects.get(user=self.request.user)  # Убедимся, что автор существует
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


class CategoryListView(ListView):
    model=Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'


    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('date_in')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subcribe(request, pk):
    user = request.user
    category = Category.objects.get(id = pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})

class CategoryViewset(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer

class PostViewest(viewsets.ModelViewSet):
   queryset = Post.objects.all()
   serializer_class = PostSerializer
   permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class Index(View):
    def get(self, request):
        curent_time = pytz.timezone.now()

        # .  Translators: This message appears on the home page only
        models = Post.objects.all()

        context = {
            'models': models,
            'current_time': pytz.timezone.now(),
            'timezones': pytz.common_timezones,  # добавляем в контекст все доступные часовые пояса
            'redirect_to': request.path,
        }

        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META['HTTP.REFERER'])