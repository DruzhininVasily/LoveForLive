from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page_views, name='home'),
    path('consultation', views.consultation, name='consultation'),
    path('articles', views.ShowAllArticles.as_view(), name='articles'),
    path('article/<int:pk>', views.ShowArticleDetail.as_view(), name='article-detail'),
    path('contacts', views.contacts_page, name='contacts'),
    path('receipts', views.ShowAllReceipts.as_view(), name='receipts'),
    path('receipt/<int:pk>', views.ShowReceiptDetail.as_view(), name='receipt-detail'),
    path('streaming/', views.get_streaming, name='main_stream')
]
