from django.urls import path
from .views import News, NewsDetail, PostCreate, Post_Search, PostUpdate, PostDelete, CategoryListView, subcribe
from django.urls import include

urlpatterns = [

   path('', News.as_view(), name='post_list'),
   path('<int:pk>/', NewsDetail.as_view(), name='post_detail'),
   path('search/', Post_Search.as_view()),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('articles/create', PostCreate.as_view(), name='articles_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_news_list'),
   path('categories/<int:pk>/subscribe', subcribe, name='subscribe'),
]


