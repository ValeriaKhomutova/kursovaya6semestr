from django.urls import path
from .views import (
    ArticleCreate,
    ArticleList,
    MyArticleList,
    ArticleUpdate,
    ArticleDelete,
)


urlpatterns = [
    path('article/create/', ArticleCreate.as_view(), name='create'),
    path('article/list/', ArticleList.as_view(), name='list'),
    path('article/mylist/', MyArticleList.as_view(), name='mylist'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),
]