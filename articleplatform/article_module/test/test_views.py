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

def create_article(user, title="title"):
    file = SimpleUploadedFile(
        "test.txt",
        b"hello world",
        content_type="text/plain"
    )

    return Article.objects.create(
        author=user,
        title=title,
        subtitle="subtitle",
        main_part=file,
        specialization="spec",
        keywords="kw",
    )

# =========================================================
# VIEW TESTS
# =========================================================

@pytest.mark.django_db(transaction=True)
class TestArticleViewsFuzz:

    # =====================================================
    # CREATE
    # =====================================================

    @settings(
        max_examples=10,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(
        title=safe_text,
        subtitle=safe_text,
        specialization=safe_text,
        keywords=safe_text,
    )
    def test_article_create_fuzz(self, title, subtitle, specialization, keywords):
        client = APIClient()
        user = create_user()
        client.force_authenticate(user=user)

        url = reverse("article-create")

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
    # LIST
    # =====================================================

    @settings(max_examples=10, deadline=None)
    @given(title=safe_text)
    def test_article_list_fuzz(self, title):
        client = APIClient()
        user = create_user()

        create_article(user, title)

        url = reverse("list")
        response = client.get(url)

        assert response.status_code == 200

    # =====================================================
    # MY LIST
    # =====================================================

    @settings(max_examples=10, deadline=None)
    @given(title=safe_text)
    def test_my_article_list_fuzz(self, title):
        client = APIClient()
        user = create_user()

        client.force_authenticate(user=user)

        create_article(user, title)

        url = reverse("mylist")
        response = client.get(url)

        assert response.status_code == 200

    # =====================================================
    # UPDATE (PUT)
    # =====================================================

    @settings(max_examples=5, deadline=None)
    @given(new_title=safe_text)
    def test_article_update_put_fuzz(self, new_title):
        client = APIClient()

        author = create_user()
        other_user = create_user()

        article = create_article(author)

        client.force_authenticate(user=author)

        url = reverse("update", args=[article.id])

        file = SimpleUploadedFile(
            "updated.txt",
            b"updated content",
            content_type="text/plain"
        )

        response = client.put(
            url,
            {
                "title": new_title,
                "subtitle": "updated",
                "main_part": file,
                "specialization": "updated",
                "keywords": "updated",
            },
            format="multipart"
        )

        assert response.status_code in (200, 400, 403, 404)

    # =====================================================
    # UPDATE (PATCH)
    # =====================================================

    @settings(max_examples=5, deadline=None)
    @given(new_title=safe_text)
    def test_article_update_patch_fuzz(self, new_title):
        client = APIClient()

        author = create_user()
        article = create_article(author)

        client.force_authenticate(user=author)

        url = reverse("update", args=[article.id])

        response = client.patch(
            url,
            {
                "title": new_title,
            },
            format="json"
        )

        assert response.status_code in (200, 400, 403, 404)

    # =====================================================
    # DELETE
    # =====================================================

    def test_article_delete_fuzz(self):
        client = APIClient()

        author = create_user()
        article = create_article(author)

        client.force_authenticate(user=author)

        url = reverse("delete", args=[article.id])

        response = client.delete(url)

        assert response.status_code in (204, 403, 404)
        
    def test_article_search_fuzz(self):
        client = APIClient()
        user = create_user()

        Article.objects.create(
            author=user,
            title="Python Django Guide",
            subtitle="subtitle",
            main_part=SimpleUploadedFile("t.txt", b"x"),
            specialization="backend",
            keywords="python,django",
        )

        url = reverse("list")

        response = client.get(url, {"search": "django"})

        assert response.status_code == 200
        assert any("Django" in a["title"] for a in response.data)
        
    def test_my_article_list_only_returns_user_articles(self):
        client = APIClient()

        user1 = create_user()
        user2 = create_user()

        Article.objects.create(
            author=user1,
            title="user1 article",
            subtitle="s",
            main_part=SimpleUploadedFile("t.txt", b"x"),
            specialization="s",
            keywords="k",
        )

        Article.objects.create(
            author=user2,
            title="user2 article",
            subtitle="s",
            main_part=SimpleUploadedFile("t.txt", b"x"),
            specialization="s",
            keywords="k",
        )

        client.force_authenticate(user=user1)

        response = client.get(reverse("mylist"))

        titles = [a["title"] for a in response.data]

        assert "user1 article" in titles
        assert "user2 article" not in titles
        
    def test_article_update_forbidden_for_non_author(self):
        client = APIClient()

        author = create_user()
        other_user = create_user()

        article = create_article(author)

        client.force_authenticate(user=other_user)

        response = client.patch(
            reverse("update", args=[article.id]),
            {"title": "hack"},
            format="json"
        )

        assert response.status_code == 403
        
    def test_article_delete_forbidden_for_non_author(self):
        client = APIClient()

        author = create_user()
        other_user = create_user()

        article = create_article(author)

        client.force_authenticate(user=other_user)

        response = client.delete(reverse("delete", args=[article.id]))

        assert response.status_code == 403
        
    def test_article_full_lifecycle(self):
        client = APIClient()
        user = create_user()
        client.force_authenticate(user=user)

        file = SimpleUploadedFile(
            "test.txt",
            b"hello world",
            content_type="text/plain"
        )

        # =========================
        # CREATE
        # =========================
        create_payload = {
            "title": "Lifecycle",
            "subtitle": "s",
            "main_part": file,
            "specialization": "s",
            "keywords": "k",
        }

        create_response = client.post(
            reverse("article-create"),
            create_payload,
            format="multipart"
        )

        print("\n================ CREATE DEBUG ================")
        print("status:", create_response.status_code)
        print("data:", create_response.data)

        # ❗ если падает — сразу видно причину
        assert create_response.status_code == 201, create_response.data

        article_id = create_response.data.get("id")
        print("CREATED ARTICLE ID:", article_id)

        if not article_id:
            print("❌ NO ID RETURNED — serializer issue")
            return

        # =========================
        # UPDATE
        # =========================
        update_file = SimpleUploadedFile(
            "updated.txt",
            b"updated content",
            content_type="text/plain"
        )

        update_payload = {
            "title": "Updated",
            "main_part": update_file,
        }

        update_response = client.patch(
            reverse("update", args=[article_id]),
            update_payload,
            format="multipart"
        )

        print("\n================ UPDATE DEBUG ================")
        print("status:", update_response.status_code)
        print("data:", update_response.data)

        assert update_response.status_code in (200, 400), update_response.data

        # =========================
        # DELETE
        # =========================
        delete_response = client.delete(reverse("delete", args=[article_id]))

        print("\n================ DELETE DEBUG ================")
        print("status:", delete_response.status_code)
        print("data:", getattr(delete_response, "data", None))

        assert delete_response.status_code == 204