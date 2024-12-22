from django.urls import path
from .views import News, NewsDetail


urlpatterns = [

   path('', News.as_view()),
   path('<int:pk>/', NewsDetail.as_view())
]