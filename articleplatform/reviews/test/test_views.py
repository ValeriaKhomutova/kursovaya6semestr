import uuid
import pytest

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from hypothesis import (
    given,
    settings,
    strategies as st,
    HealthCheck,
)

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

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

# =========================================================
# USER FACTORY
# =========================================================

def create_user():
    return User.objects.create_user(
        email=f"{uuid.uuid4()}@test.com",
        password="test123S1!",
        name="John",
        surname="Doe",
        telephone="+123456789",
    )

# =========================================================
# REVIEW VIEW TESTS
# =========================================================

@pytest.mark.django_db(transaction=True)
class TestReviewViewsFuzz:

    # =====================================================
    # REVIEW CREATE
    # =====================================================

    @settings(
        max_examples=10,
        deadline=None,
        suppress_health_check=[
            HealthCheck.function_scoped_fixture,
        ],
    )
    @given(
        text=safe_text,
        like=st.booleans(),
        dislike=st.booleans(),
    )
    def test_review_create_fuzz(
        self,
        text,
        like,
        dislike,
    ):
        client = APIClient()

        user = create_user()

        client.force_authenticate(user=user)

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world",
            content_type="text/plain"
        )

        article = Article.objects.create(
            author=user,
            title="title",
            subtitle="subtitle",
            main_part=file,
            specialization="spec",
            keywords="kw",
        )

        url = reverse("create")

        response = client.post(
            url,
            {
                "article": article.id,
                "text": text,
                "like": like,
                "dislike": dislike,
            },
            format="json"
        )

        assert response.status_code in (201, 400)

    # =====================================================
    # REVIEW DELETE
    # =====================================================

    @settings(
        max_examples=10,
        deadline=None,
    )
    @given(
        text=safe_text,
    )
    def test_review_delete_fuzz(
        self,
        text,
    ):
        client = APIClient()

        user = create_user()

        client.force_authenticate(user=user)

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world",
            content_type="text/plain"
        )

        article = Article.objects.create(
            author=user,
            title="title",
            subtitle="subtitle",
            main_part=file,
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

        url = f"/reviews/api/v1/reviews/{review.id}/"

        response = client.delete(url)

        assert response.status_code in (
            204,
            403,
            404,
        )