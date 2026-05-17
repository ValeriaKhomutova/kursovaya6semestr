const API_URL = "/article_module/api/v1";
const REVIEW_URL = "/reviews/api/v1";

const container =
    document.getElementById(
        "articlesContainer"
    );

document.addEventListener("DOMContentLoaded", () => {

    initModals();
    loadArticles();

    updateAuthUI();

    document
        .getElementById("articleForm")
        .addEventListener("submit", createArticle);

    document
        .getElementById("logoutBtn")
        .addEventListener("click", logout);

    document
        .getElementById("registerBtn")
        .addEventListener("click", goToRegister);
});



function initModals() {

    const profileBtn =
        document.getElementById(
            "profileBtn"
        );

    const createBtn =
        document.getElementById(
            "createArticleBtn"
        );

    const profileModal =
        document.getElementById(
            "profileModal"
        );

    const createModal =
        document.getElementById(
            "createArticleModal"
        );

    const articleModal =
        document.getElementById(
            "articleModal"
        );



    profileBtn.addEventListener(
        "click",
        () => {

            profileModal
                .classList
                .add("active");

            loadMyArticles();
        }
    );



    createBtn.addEventListener(
        "click",
        () => {

            createModal
                .classList
                .add("active");
        }
    );



    document
        .getElementById("closeProfile")
        .addEventListener(
            "click",
            () => {

                profileModal
                    .classList
                    .remove("active");
            }
        );



    document
        .getElementById("closeCreate")
        .addEventListener(
            "click",
            () => {

                createModal
                    .classList
                    .remove("active");
            }
        );



    document
        .getElementById("closeArticle")
        .addEventListener(
            "click",
            () => {

                articleModal
                    .classList
                    .remove("active");
            }
        );



    window.addEventListener(
        "click",
        (e) => {

            if (e.target === profileModal) {

                profileModal
                    .classList
                    .remove("active");
            }

            if (e.target === createModal) {

                createModal
                    .classList
                    .remove("active");
            }

            if (e.target === articleModal) {

                articleModal
                    .classList
                    .remove("active");
            }
        }
    );
}



async function loadArticles() {

    try {

        const response =
            await fetch(
                `${API_URL}/article/list/`
            );

        const articles =
            await response.json();

        container.innerHTML = "";

        articles.forEach(article => {

            container.innerHTML += `

                <div class="article-card">

                    <div
                        class="article-top"
                        onclick='openArticle(${JSON.stringify(article)})'
                    >

                        <div class="article-title">
                            ${article.title}
                        </div>

                        <div class="article-subtitle">
                            ${article.subtitle}
                        </div>

                        <div class="article-meta">

                            <span>
                                Автор:
                                ${article.author.email}
                            </span>

                            <span>
                                Специализация:
                                ${article.specialization}
                            </span>

                            <span>
                                Отзывы:
                                ${article.reviews_count}
                            </span>

                        </div>

                        <div class="article-keywords">
                            ${article.keywords || ""}
                        </div>

                    </div>

                </div>

            `;
        });

    } catch(error) {

        container.innerHTML =
            "Ошибка загрузки статей";
    }
}



function openArticle(article) {

    const modal =
        document.getElementById(
            "articleModal"
        );

    const content =
        document.getElementById(
            "articleModalContent"
        );

    let reviewsHtml = "";

    if (article.reviews.length === 0) {

        reviewsHtml = `
            <p class="no-reviews">
                Пока нет отзывов
            </p>
        `;
    }

    else {

        article.reviews.forEach(review => {

            reviewsHtml += `

                <div class="review-card">

                    <div class="review-top">

                        <span class="review-author">
                            ${review.author.email}
                        </span>

                        <span class="review-date">
                            ${new Date(
                                review.created_at
                            ).toLocaleDateString()}
                        </span>

                    </div>

                    <div class="review-text">
                        ${review.text || ""}
                    </div>

                    <div class="review-type">

                        ${
                            review.like
                            ? "👍 Лайк"
                            : ""
                        }

                        ${
                            review.dislike
                            ? "👎 Дизлайк"
                            : ""
                        }

                    </div>

                </div>

            `;
        });
    }

    content.innerHTML = `

        <h2 class="modal-article-title">
            ${article.title}
        </h2>

        <p class="modal-article-subtitle">
            ${article.subtitle}
        </p>

        <div class="modal-article-meta">

            <span>
                Автор:
                ${article.author.email}
            </span>

            <span>
                Специализация:
                ${article.specialization}
            </span>

        </div>

        <div class="modal-keywords">
            ${article.keywords || ""}
        </div>

        <a
            href="${article.main_part}"
            target="_blank"
            class="open-file-btn"
        >
            Открыть статью
        </a>

        <div class="modal-review-buttons">

            <button
                class="action-btn like"
                onclick="sendReaction(${article.id}, true)"
            >
                👍 ${article.likes}
            </button>

            <button
                class="action-btn dislike"
                onclick="sendReaction(${article.id}, false)"
            >
                👎 ${article.dislikes}
            </button>

        </div>

        <div class="reviews-section">

            <h3>
                Отзывы
                (${article.reviews_count})
            </h3>

            <div class="reviews-list">
                ${reviewsHtml}
            </div>

        </div>

        <div class="create-review">

            <h3>
                Оставить отзыв
            </h3>

            <textarea
                id="reviewText"
                placeholder="Напишите отзыв..."
            ></textarea>

            <div class="review-select">

                <label>
                    <input
                        type="radio"
                        name="reviewType"
                        value="like"
                        checked
                    >
                    👍 Лайк
                </label>

                <label>
                    <input
                        type="radio"
                        name="reviewType"
                        value="dislike"
                    >
                    👎 Дизлайк
                </label>

            </div>

            <button
                class="submit-review-btn"
                onclick="submitReview(${article.id})"
            >
                Отправить отзыв
            </button>

        </div>

    `;

    modal.classList.add("active");
}



async function sendReaction(
    articleId,
    isLike
) {

    const token =
        localStorage.getItem("access");

    try {

        await fetch(
            `${REVIEW_URL}/review/create/`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({
                    article: articleId,
                    text: "",
                    like: isLike,
                    dislike: !isLike
                })
            }
        );

        await loadArticles();

        // обновить открытую статью
        const response =
            await fetch(
                `${API_URL}/article/list/`
            );

        const articles =
            await response.json();

        const updatedArticle =
            articles.find(
                a => a.id === articleId
            );

        if (updatedArticle) {

            openArticle(updatedArticle);
        }

    } catch(error) {

        console.log(error);
    }
}


async function submitReview(articleId) {

    const token =
        localStorage.getItem("access");

    const text =
        document.getElementById(
            "reviewText"
        ).value;

    const type =
        document.querySelector(
            'input[name="reviewType"]:checked'
        ).value;

    try {

        await fetch(
            `${REVIEW_URL}/review/create/`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({

                    article: articleId,

                    text: text,

                    like: type === "like",

                    dislike: type === "dislike"
                })
            }
        );

        await loadArticles();

        const response =
            await fetch(
                `${API_URL}/article/list/`
            );

        const articles =
            await response.json();

        const updatedArticle =
            articles.find(
                a => a.id === articleId
            );

        openArticle(updatedArticle);

    } catch(error) {

        console.log(error);

        alert(
            "Ошибка отправки отзыва"
        );
    }
}


async function loadMyArticles() {

    const token = localStorage.getItem("access");

    const container =
        document.getElementById("myArticles");

    try {

        // 🔥 берём данные ИЗ JWT
        const me = parseJwt(token);

        // статьи остаются как у тебя было
        const articlesResponse = await fetch(
            `${API_URL}/article/mylist/`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const articles = await articlesResponse.json();

        let articlesHtml = "";

        if (articles.length === 0) {
            articlesHtml = "<p>У вас пока нет статей</p>";
        } else {
            articles.forEach(article => {
                articlesHtml += `
                    <div class="my-article">
                        <h3>${article.title}</h3>
                        <p>${article.subtitle}</p>
                    </div>
                `;
            });
        }

        container.innerHTML = `
            <div class="profile-data">
                <p><b>Email:</b> ${me.email || "—"}</p>
                <p><b>Username:</b> ${me.name || "—"}</p>
            </div>

            <hr>

            <div class="profile-articles">
                <h3>Мои статьи</h3>
                ${articlesHtml}
            </div>
        `;

    } catch (error) {
        console.log(error);
        container.innerHTML = "<p>Ошибка загрузки профиля</p>";
    }
}

async function createArticle(e) {

    e.preventDefault();

    const token =
        localStorage.getItem("access");

    const formData =
        new FormData();

    formData.append(
        "title",
        document
            .getElementById("title")
            .value
    );

    formData.append(
        "subtitle",
        document
            .getElementById("subtitle")
            .value
    );

    formData.append(
        "specialization",
        document
            .getElementById("specialization")
            .value
    );

    formData.append(
        "keywords",
        document
            .getElementById("keywords")
            .value
    );

    formData.append(
        "main_part",
        document
            .getElementById("main_part")
            .files[0]
    );

    try {

        const response =
            await fetch(
                `${API_URL}/article/create/`,
                {
                    method: "POST",

                    headers: {
                        "Authorization":
                            `Bearer ${token}`
                    },

                    body: formData
                }
            );

        if (!response.ok) {

            const error =
                await response.json();

            console.log(error);

            throw new Error();
        }

        alert("Статья создана");

        document
            .getElementById(
                "createArticleModal"
            )
            .classList
            .remove("active");

        document
            .getElementById(
                "articleForm"
            )
            .reset();

        loadArticles();

    } catch(error) {

        console.log(error);

        alert(
            "Ошибка создания статьи"
        );
    }
}


function isAuth() {
    return !!localStorage.getItem("access");
}

function updateAuthUI() {

    const logoutBtn = document.getElementById("logoutBtn");
    const registerBtn = document.getElementById("registerBtn");

    if (isAuth()) {

        logoutBtn.style.display = "inline-block";
        registerBtn.style.display = "none";

    } else {

        logoutBtn.style.display = "none";
        registerBtn.style.display = "inline-block";
    }
}

function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.reload();
}

function goToRegister() {
    window.location.href = "/register/";
}

function parseJwt(token) {
    if (!token) return null;

    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return null;
    }
}