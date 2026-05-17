from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Review


User = get_user_model()




class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'surname',
            'telephone',
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'article',
            'text',
            'like',
            'dislike',
        ]

    def validate(self, attrs):
        like = attrs.get('like', False)
        dislike = attrs.get('dislike', False)

        if like and dislike:
            raise serializers.ValidationError(
                "Нельзя одновременно поставить like и dislike"
            )
        
        if not like and not dislike:
            raise serializers.ValidationError(
                "Нужно выбрать like или dislike"
            )

        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'text',
            'like',
            'dislike',
            'created_at',
        ]
        read_only_fields = ['author', 'created_at']