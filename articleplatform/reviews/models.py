from django.db import models
from django.conf import settings


class Review(models.Model):
    article = models.ForeignKey(
        'article_module.Article',
        on_delete=models.CASCADE,
        related_name='reviews'
    )   

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.email}"