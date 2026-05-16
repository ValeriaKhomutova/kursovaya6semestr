const API_URL = "/users/api/v1";

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const message = document.getElementById("message");

function showForm(type) {
    const tabs = document.querySelectorAll(".tab");

    tabs.forEach(tab => tab.classList.remove("active"));

    if (type === "login") {
        loginForm.classList.remove("hidden");
        registerForm.classList.add("hidden");
        tabs[0].classList.add("active");
    } else {
        registerForm.classList.remove("hidden");
        loginForm.classList.add("hidden");
        tabs[1].classList.add("active");
    }

    message.innerHTML = "";
}

function showMessage(text, type) {
    message.innerHTML = `<span class="${type}">${text}</span>`;
}

function redirectHome() {
    window.location.href = "/";
}

/* LOGIN */

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        email: loginEmail.value,
        password: loginPassword.value
    };

    try {
        const response = await fetch(`${API_URL}/login/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("access", result.access);
            localStorage.setItem("refresh", result.refresh);

            showMessage("Успешный вход...", "success");

            setTimeout(() => {
                redirectHome();
            }, 700);

        } else {
            showMessage("Неверный email или пароль", "error");
        }

    } catch {
        showMessage("Ошибка сервера", "error");
    }
});


/* REGISTER */

registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        email: regEmail.value,
        name: regName.value,
        surname: regSurname.value,
        telephone: regPhone.value,
        password: regPassword.value
    };

    try {
        const response = await fetch(`${API_URL}/register/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("access", result.access);
            localStorage.setItem("refresh", result.refresh);

            showMessage("Регистрация успешна...", "success");

            setTimeout(() => {
                redirectHome();
            }, 700);

        } else {
            showMessage("Ошибка регистрации", "error");
        }

    } catch {
        showMessage("Ошибка сервера", "error");
    }
});