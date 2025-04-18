from django.urls import path
from .views import News, NewsDetail, PostCreate, Post_Search, PostUpdate, PostDelete, CategoryListView, subcribe
from django.urls import include
from django.views.decorators.cache import cache_page

urlpatterns = [

   path('', cache_page(60*5)(News.as_view()), name='post_list'),
   path('<int:pk>/', cache_page(60*5)(NewsDetail.as_view()), name='post_detail'),
   path('search/', Post_Search.as_view()),
   path('create/', cache_page(60*10)(PostCreate.as_view()), name='news_create'),
   path('articles/create', cache_page(60*10)(PostCreate.as_view()), name='articles_create'),
   path('<int:pk>/edit/', cache_page(60*10)(PostUpdate.as_view()), name='news_edit'),
   path('articles/<int:pk>/edit/', cache_page(60*10)(PostUpdate.as_view()), name='articles_edit'),
   path('<int:pk>/delete/', cache_page(60*10)(PostDelete.as_view()), name='news_delete'),
   path('<int:pk>/delete/', cache_page(60*10)(PostDelete.as_view()), name='articles_delete'),
   path('categories/<int:pk>', cache_page(60*10)(CategoryListView.as_view()), name='category_news_list'),
   path('categories/<int:pk>/subscribe', subcribe, name='subscribe'),

]


