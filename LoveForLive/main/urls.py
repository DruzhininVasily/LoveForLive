from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page_views, name='home'),
    path('articles', views.ShowAllArticles.as_view(), name='articles'),
    path('article/<int:pk>', views.ShowArticleDetail.as_view(), name='article-detail'),
    path('streaming/', views.get_streaming, name='main_stream')
]
