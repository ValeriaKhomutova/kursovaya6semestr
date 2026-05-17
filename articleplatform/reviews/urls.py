from django.urls import path
from .views import ReviewCreate, ReviewDelete


urlpatterns = [
    path('review/create/', ReviewCreate.as_view(), name='create'),
    path('reviews/<int:pk>/', ReviewDelete.as_view()),
]