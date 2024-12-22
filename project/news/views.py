from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post

class News(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        #context['next_sale'] = None
        return context
class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'
