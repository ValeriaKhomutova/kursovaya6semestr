from rest_framework import serializers
from django.db.models import Sum, Case, When, IntegerField
from django.contrib.auth import get_user_model

from .models import Article
from reviews.models import Review

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

class ArticleSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)

    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)

    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'subtitle',
            'main_part',
            'specialization',
            'keywords',

            'author',

            'reviews',
            'reviews_count',

            'likes',
            'dislikes',
        ]

    def get_likes(self, obj):
        return obj.reviews.aggregate(
            total=Sum(
                Case(
                    When(like=True, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['total'] or 0

    def get_dislikes(self, obj):
        return obj.reviews.aggregate(
            total=Sum(
                Case(
                    When(dislike=True, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['total'] or 0