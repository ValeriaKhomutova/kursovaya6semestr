from django.urls import path
from .views import ArticleCreate, ArticleList, MyArticleList


urlpatterns = [
    path('article/create/', ArticleCreate.as_view(), name='create'),
    path('article/list/', ArticleList.as_view(), name='list'),
    path('article/mylist/', MyArticleList.as_view(), name='mylist'),
]