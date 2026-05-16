const API_URL = "/article_module/api/v1";
const REVIEW_URL = "/reviews/api/v1";

const container = document.getElementById("articlesContainer");

document.addEventListener("DOMContentLoaded", loadArticles);

async function loadArticles() {
    try {
        const response = await fetch(`${API_URL}/article/list/`);
        const articles = await response.json();

        container.innerHTML = "";

        articles.forEach(article => {
            container.innerHTML += `
                <div class="article-card">

                    <div class="article-top" onclick="openArticle(${article.id})">

                        <div class="article-title">${article.title}</div>

                        <div class="article-subtitle">
                            ${article.subtitle}
                        </div>

                        <div class="article-meta">
                            <span>Автор: ${article.author.email}</span>
                            <span>Специализация: ${article.specialization}</span>
                            <span>Отзывы: ${article.reviews_count}</span>
                        </div>

                        <div class="article-keywords">
                            ${article.keywords || ""}
                        </div>

                    </div>

                    <div class="article-actions">

                        <button class="action-btn like"
                        onclick="sendReaction(${article.id}, true)">
                            👍 ${article.likes}
                        </button>

                        <button class="action-btn dislike"
                        onclick="sendReaction(${article.id}, false)">
                            👎 ${article.dislikes}
                        </button>

                        <button class="action-btn review"
                        onclick="leaveReview(${article.id})">
                            Оставить отзыв
                        </button>

                    </div>

                </div>
            `;
        });

    } catch(error) {
        container.innerHTML = "Ошибка загрузки статей";
    }
}

function goProfile() {
    window.location.href = "/profile/";
}

function goCreateArticle() {
    window.location.href = "/create-article/";
}

function openArticle(id) {
    window.location.href = `/article/${id}/`;
}

async function sendReaction(articleId, isLike) {
    const token = localStorage.getItem("access");

    const text = isLike ? "Like" : "Dislike";

    await fetch(`${REVIEW_URL}/review/create/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            article: articleId,
            text: text,
            like: isLike,
            dislike: !isLike
        })
    });

    loadArticles();
}

async function leaveReview(articleId) {
    const token = localStorage.getItem("access");

    const text = prompt("Введите отзыв:");

    if (!text) return;

    await fetch(`${REVIEW_URL}/review/create/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            article: articleId,
            text: text,
            like: true,
            dislike: false
        })
    });

    loadArticles();
}