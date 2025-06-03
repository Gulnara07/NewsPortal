from django.contrib import admin
from django.urls import path, include
#from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'news', views.PostViewest, basename='news')

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('news.urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   #path('', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   #path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),
   path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
   path('', include('sign.urls')),
      ]
admin.site.site_header = 'Администрирование News Portal'
admin.site.index_title = 'Новостной портал'