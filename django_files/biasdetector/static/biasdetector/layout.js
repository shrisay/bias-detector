const html = document.querySelector("html");
const toggle = document.querySelector("#darkModeToggle");
const submit = document.querySelector("#submit");
const biasButton = document.querySelector("#bias-button");
const aboutButton = document.querySelector("#about-button");
const workButton = document.querySelector("#work-button");

document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("theme")) {
        html.setAttribute("data-bs-theme", localStorage.getItem("theme"));
    }
    updateButton();

    toggle.addEventListener("click", () => {
        let isDark = html.getAttribute("data-bs-theme") === "dark";
        html.setAttribute("data-bs-theme", isDark ? "light" : "dark");

        updateButton();    
        localStorage.setItem("theme", isDark ? "light" : "dark");
    });

    document.addEventListener("DOMContentLoaded", () => {
        const forms = document.querySelectorAll("form");
        forms.forEach(form => {
            form.addEventListener("submit", () => {
                const submitButtons = form.querySelectorAll('button[type="submit"]');
                submitButtons.forEach(btn => {
                    btn.disabled = true;
                    btn.innerText = "Submitting...";
                });
            });
        });
    });   
});

function updateButton() {
    let isDark = html.getAttribute("data-bs-theme") === "dark";
    if (isDark) {
        toggle.classList.remove("btn-dark");
        toggle.classList.add("btn-light"); 
        toggle.textContent = "☀️ Light Mode";

        aboutButton.style.color = "white";
        workButton.style.color = "white";

        if (submit) {
            submit.classList.add("btn-light");
            submit.classList.remove("btn-dark");
        }

        if (biasButton) {
            biasButton.classList.add("btn-light");
            biasButton.classList.remove("btn-dark");
        }
            
    } else {
        toggle.classList.add("btn-dark");
        toggle.classList.remove("btn-success");
        toggle.textContent = "🌙 Dark Mode";

        aboutButton.style.color = "black";
        workButton.style.color = "black";

        if (submit) {
            submit.classList.add("btn-dark");
            submit.classList.remove("btn-success");
        } 

        if (biasButton) {
            biasButton.classList.add("btn-dark");
            biasButton.classList.remove("btn-info");
        }
    }
}