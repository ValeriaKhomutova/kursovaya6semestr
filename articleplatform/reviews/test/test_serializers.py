import uuid

import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from django.contrib.auth import get_user_model

from reviews.serializers import (
    UserPublicSerializer,
    ReviewCreateSerializer,
    ReviewSerializer,
)

from reviews.models import Review
from article_module.models import Article

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
        password="Testpass123!",
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
# REVIEW CREATE SERIALIZER
# =========================================================

@pytest.mark.django_db
@given(
    text=safe_text,
    like=st.booleans(),
    dislike=st.booleans(),
)
@fuzz_settings
def test_review_create_serializer_fuzz(
    text,
    like,
    dislike,
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
        title="title",
        subtitle="subtitle",
        main_part="content",
        specialization="spec",
        keywords="kw",
    )

    data = {
        "article": article.id,
        "text": text,
        "like": like,
        "dislike": dislike,
    }

    serializer = ReviewCreateSerializer(data=data)

    is_valid = serializer.is_valid()

    expected_valid = (
        (like and not dislike)
        or
        (dislike and not like)
    )

    assert is_valid == expected_valid

    if not expected_valid:

        if like and dislike:
            assert (
                "Нельзя одновременно поставить like и dislike"
                in str(serializer.errors)
            )

        if not like and not dislike:
            assert (
                "Нужно выбрать like или dislike"
                in str(serializer.errors)
            )


# =========================================================
# REVIEW SERIALIZER
# =========================================================

@pytest.mark.django_db
@given(
    text=safe_text,
)
@fuzz_settings
def test_review_serializer_fuzz(text):
    user = User.objects.create_user(
        email=f"{uuid.uuid4()}@test.com",
        password="testpass123",
        name="John",
        surname="Doe",
        telephone="+123456789",
    )

    article = Article.objects.create(
        author=user,
        title="title",
        subtitle="subtitle",
        main_part="content",
        specialization="spec",
        keywords="kw",
    )

    review = Review.objects.create(
        article=article,
        author=user,
        text=text,
        like=True,
        dislike=False,
    )

    serializer = ReviewSerializer(review)

    data = serializer.data

    assert data["id"] == review.id
    assert data["text"] == review.text
    assert data["like"] is True
    assert data["dislike"] is False

    assert data["author"]["id"] == user.id
    assert data["author"]["email"] == user.email