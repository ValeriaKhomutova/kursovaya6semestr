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
# VIEW TESTS
# =========================================================

@pytest.mark.django_db(transaction=True)
class TestArticleViewsFuzz:

    # =====================================================
    # ARTICLE CREATE
    # =====================================================

    @settings(
        max_examples=10,
        deadline=None,
        suppress_health_check=[
            HealthCheck.function_scoped_fixture,
        ],
    )
    @given(
        title=safe_text,
        subtitle=safe_text,
        specialization=safe_text,
        keywords=safe_text,
    )
    def test_article_create_fuzz(
        self,
        title,
        subtitle,
        specialization,
        keywords,
    ):
        client = APIClient()

        user = create_user()

        client.force_authenticate(user=user)

        url = reverse("create")

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world",
            content_type="text/plain"
        )

        response = client.post(
            url,
            {
                "title": title,
                "subtitle": subtitle,
                "main_part": file,
                "specialization": specialization,
                "keywords": keywords,
            },
            format="multipart"
        )

        assert response.status_code in (201, 400)

    # =====================================================
    # ARTICLE LIST
    # =====================================================

    @settings(
        max_examples=10,
        deadline=None,
    )
    @given(
        title=safe_text,
    )
    def test_article_list_fuzz(self, title):
        client = APIClient()

        user = create_user()

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world",
            content_type="text/plain"
        )

        Article.objects.create(
            author=user,
            title=title,
            subtitle="subtitle",
            main_part=file,
            specialization="spec",
            keywords="kw",
        )

        url = reverse("list")

        response = client.get(url)

        assert response.status_code == 200

    # =====================================================
    # MY ARTICLE LIST
    # =====================================================

    @settings(
        max_examples=10,
        deadline=None,
    )
    @given(
        title=safe_text,
    )
    def test_my_article_list_fuzz(self, title):
        client = APIClient()

        user = create_user()

        client.force_authenticate(user=user)

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world",
            content_type="text/plain"
        )

        Article.objects.create(
            author=user,
            title=title,
            subtitle="subtitle",
            main_part=file,
            specialization="spec",
            keywords="kw",
        )

        url = reverse("mylist")

        response = client.get(url)

        assert response.status_code == 200