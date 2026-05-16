from django.db import models
from django.conf import settings

class Article(models.Model):

    title = models.CharField(max_length=255)

    subtitle = models.CharField(max_length=255)

    main_part = models.FileField(upload_to='files/')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    specialization = models.CharField(max_length=100)

    keywords = models.CharField(max_length=255, blank=True)

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

