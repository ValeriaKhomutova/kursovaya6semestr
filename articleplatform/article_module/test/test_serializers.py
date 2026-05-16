import uuid

import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from django.contrib.auth import get_user_model

from article_module.serializers import (
    UserPublicSerializer,
    ArticleSerializer,
)

from article_module.models import Article
from reviews.models import Review

User = get_user_model()

# =========================================================
# SAFE STRATEGIES
# =========================================================

safe_text = st.text(
    alphabet=(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        " абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        "-_.,!?()"
    ),
    min_size=1,
    max_size=30,
)

emails = st.builds(lambda: f"{uuid.uuid4()}@test.com")

telephones = st.text(
    alphabet="0123456789+-() ",
    min_size=5,
    max_size=20,
)

# =========================================================
# HYPOTHESIS SETTINGS
# =========================================================

fuzz_settings = settings(
    max_examples=20,
    deadline=None,
    suppress_health_check=[
        HealthCheck.function_scoped_fixture,
        HealthCheck.too_slow,
    ],
)

# =========================================================
# USER SERIALIZER
# =========================================================

@pytest.mark.django_db
@given(
    email=emails,
    name=safe_text,
    surname=safe_text,
    telephone=telephones,
)
@fuzz_settings
def test_user_public_serializer_fuzz(
    email,
    name,
    surname,
    telephone,
):
    user = User.objects.create_user(
        email=email,
        password="testpass123",
        name=name,
        surname=surname,
        telephone=telephone,
    )

    serializer = UserPublicSerializer(user)

    data = serializer.data

    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["name"] == user.name
    assert data["surname"] == user.surname
    assert data["telephone"] == user.telephone


# =========================================================
# ARTICLE SERIALIZER
# =========================================================

@pytest.mark.django_db
@given(
    title=safe_text,
    subtitle=safe_text,
    main_part=safe_text,
    specialization=safe_text,
    keywords=safe_text,
)
@fuzz_settings
def test_article_serializer_fuzz(
    title,
    subtitle,
    main_part,
    specialization,
    keywords,
):
    user = User.objects.create_user(
        email=f"{uuid.uuid4()}@test.com",
        password="testpass123",
        name="John",
        surname="Doe",
        telephone="+123456789",
    )

    article = Article.objects.create(
        author=user,
        title=title,
        subtitle=subtitle,
        main_part=main_part,
        specialization=specialization,
        keywords=keywords,
    )

    likes_count = 0
    dislikes_count = 0

    for i in range(4):
        if i % 2 == 0:
            like = True
            dislike = False
            likes_count += 1
        else:
            like = False
            dislike = True
            dislikes_count += 1

        Review.objects.create(
            article=article,
            author=user,
            text="review",
            like=like,
            dislike=dislike,
        )

    serializer = ArticleSerializer(article)

    data = serializer.data

    assert data["id"] == article.id
    assert data["title"] == article.title
    assert data["subtitle"] == article.subtitle
    assert isinstance(data["main_part"], str)
    assert data["specialization"] == article.specialization
    assert data["keywords"] == article.keywords

    assert data["author"]["id"] == user.id

    assert data["reviews_count"] == 4
    assert data["likes"] == likes_count
    assert data["dislikes"] == dislikes_count

    assert len(data["reviews"]) == 4