const API_URL = "/article_module/api/v1";
const REVIEW_URL = "/reviews/api/v1";
let editingArticleId = null;
let isEditMode = false;
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
        .addEventListener("submit", handleArticleSubmit);

    document
        .getElementById("logoutBtn")
        .addEventListener("click", logout);

    document
        .getElementById("registerBtn")
        .addEventListener("click", goToRegister);

    document.getElementById("confirmDeleteBtn")
        .addEventListener("click", deleteArticle);

    document.getElementById("cancelDeleteBtn")
        .addEventListener("click", closeDeleteModal);
    

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

            resetArticleForm();

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
            closeArticleForm
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
                closeArticleForm();
            }

            if (e.target === articleModal) {

                articleModal
                    .classList
                    .remove("active");
            }
            const deleteModal = document.getElementById("deleteModal");
            if (e.target === deleteModal) {
                closeDeleteModal();
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
    const container = document.getElementById("myArticles");

    try {

        const me = parseJwt(token);

        const response = await fetch(
            `${API_URL}/article/mylist/`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const articles = await response.json();

        let html = "";

        if (articles.length === 0) {
            html = "<p>У вас пока нет статей</p>";
        } else {

            articles.forEach(article => {
                html += `
                    <div class="my-article">

                        <h3>${article.title}</h3>
                        <p>${article.subtitle}</p>

                        <div class="article-actions">

                            <button class="action-btn review"
                                onclick="openEditArticle(${article.id})">
                                Редактировать
                            </button>

                            <button class="action-btn dislike"
                                onclick="openDeleteModal(${article.id})">
                                Удалить
                            </button>

                        </div>

                    </div>
                `;
            });
        }

        container.innerHTML = `
            <div class="profile-data">
                <p><b>Email:</b> ${me?.email || "—"}</p>
                <p><b>Username:</b> ${me?.name || "—"}</p>
            </div>

            <hr>

            <div class="profile-articles">
                <h3>Мои статьи</h3>
                ${html}
            </div>
        `;

    } catch (error) {
        console.log(error);
        container.innerHTML = "<p>Ошибка загрузки профиля</p>";
    }
}


async function handleArticleSubmit(e) {

    e.preventDefault();

    if (isEditMode) {
        await updateArticle();
    } else {
        await createArticle();
    }
}

async function createArticle() {

    const token = localStorage.getItem("access");

    const formData = new FormData();

    formData.append(
        "title",
        document.getElementById("title").value
    );

    formData.append(
        "subtitle",
        document.getElementById("subtitle").value
    );

    formData.append(
        "specialization",
        document.getElementById("specialization").value
    );

    formData.append(
        "keywords",
        document.getElementById("keywords").value
    );

    const file =
        document.getElementById("main_part").files[0];

    if (file) {
        formData.append("main_part", file);
    }

    try {

        const response = await fetch(
            `${API_URL}/article/create/`,
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error();
        }

        showToast("Статья создана");

        closeArticleForm();

        loadArticles();
        loadMyArticles();

    } catch(error) {

        console.log(error);

        showToast("Ошибка создания статьи", "error");
    }
}


async function updateArticle() {

    const token = localStorage.getItem("access");

    const formData = new FormData();

    formData.append(
        "title",
        document.getElementById("title").value
    );

    formData.append(
        "subtitle",
        document.getElementById("subtitle").value
    );

    formData.append(
        "specialization",
        document.getElementById("specialization").value
    );

    formData.append(
        "keywords",
        document.getElementById("keywords").value
    );

    const file =
        document.getElementById("main_part").files[0];

    if (file) {
        formData.append("main_part", file);
    }

    try {

        const response = await fetch(
            `${API_URL}/article/${editingArticleId}/update/`,
            {
                method: "PATCH",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error();
        }

        showToast("Статья обновлена");

        closeArticleForm();

        loadArticles();
        loadMyArticles();

    } catch(error) {

        console.log(error);

        showToast("Ошибка обновления", "error");
    }
}

function isAuth() {
    return !!localStorage.getItem("access");
}

function updateAuthUI() {

    const logoutBtn =
        document.getElementById("logoutBtn");

    const registerBtn =
        document.getElementById("registerBtn");

    const createArticleBtn =
        document.getElementById("createArticleBtn");

    const profileBtn =
        document.getElementById("profileBtn");

    if (isAuth()) {

        logoutBtn.style.display = "inline-block";

        registerBtn.style.display = "none";

        createArticleBtn.style.display = "inline-block";

        profileBtn.style.display = "inline-block";

    } else {

        logoutBtn.style.display = "none";

        registerBtn.style.display = "inline-block";

        createArticleBtn.style.display = "none";

        profileBtn.style.display = "none";
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


async function searchArticles(query) {
    try {
        const response = await fetch(
            `${API_URL}/article/list/?search=${encodeURIComponent(query)}`
        );

        const articles = await response.json();

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

    } catch (error) {
        console.log(error);
        container.innerHTML = "Ошибка поиска";
    }
}

let searchTimeout;

document.getElementById("searchInput")
    .addEventListener("input", (e) => {

        const value = e.target.value.trim();

        clearTimeout(searchTimeout);

        searchTimeout = setTimeout(() => {

            if (value === "") {
                loadArticles(); // показать все статьи
            } else {
                searchArticles(value); // поиск
            }

        }, 100);

    });



async function deleteArticle() {

    const btn = document.getElementById("confirmDeleteBtn");
    btn.disabled = true;

    const token = localStorage.getItem("access");

    try {

        const response = await fetch(
            `${API_URL}/article/${deletingArticleId}/delete/`,
            {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) throw new Error();

        closeDeleteModal();

        showToast("Статья удалена");

        loadArticles();
        loadMyArticles();

    } catch (error) {

        console.log(error);
        showToast("Ошибка удаления", "error");

    } finally {
        btn.disabled = false;
    }
}
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.textContent = message;
    toast.className = "toast show";

    if (type === "error") {
        toast.classList.add("error");
    }

    setTimeout(() => {
        toast.className = "toast";
    }, 2000);
}

let deletingArticleId = null;


function openDeleteModal(articleId) {
    deletingArticleId = articleId;

    document
        .getElementById("deleteModal")
        .classList.add("active");
}


function closeDeleteModal() {
    document
        .getElementById("deleteModal")
        .classList.remove("active");

    deletingArticleId = null;
}


async function openEditArticle(id) {

    try {

        const response =
            await fetch(`${API_URL}/article/list/`);

        const articles =
            await response.json();

        const article =
            articles.find(a => a.id === id);

        if (!article) return;

        editingArticleId = id;
        isEditMode = true;

        document.getElementById("title").value =
            article.title;

        document.getElementById("subtitle").value =
            article.subtitle;

        document.getElementById("specialization").value =
            article.specialization;

        document.getElementById("keywords").value =
            article.keywords || "";

        document.getElementById("main_part").required = false;

        document.querySelector(
            "#articleForm button[type='submit']"
        ).textContent = "Сохранить";

        document.querySelector(
            "#createArticleModal h2"
        ).textContent = "Редактировать статью";

        document.getElementById(
            "createArticleModal"
        ).classList.add("active");

    } catch (e) {

        console.log(e);
    }
}

function resetArticleForm() {

    isEditMode = false;
    editingArticleId = null;

    document.getElementById("articleForm").reset();

    document.getElementById("main_part").required = true;

    document.querySelector(
        "#articleForm button[type='submit']"
    ).textContent = "Создать";

    document.querySelector(
        "#createArticleModal h2"
    ).textContent = "Создать статью";
}

function closeArticleForm() {

    document
        .getElementById("createArticleModal")
        .classList.remove("active");

    resetArticleForm();
}