// Datei-Header: JS-Logik für die Startseite (Authentifizierung, UI, Interaktionen)
// CSRF-Cookie vom Server anfordern (beim Start)
fetch("http://localhost:8000/api/casino/session/", { credentials: "include" });

// Funktion: getCookie(name)
// Liest ein Cookie aus `document.cookie` aus und gibt den Wert des angegebenen
// Cookie-Namens zurück (z. B. CSRF-Token). Gibt `undefined` zurück, wenn nicht gefunden.
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// DOM Elements
const authSection = document.getElementById("auth-section");
const welcomeSection = document.getElementById("welcome-section");
const loginSection = document.getElementById("login-section");
const registerSection = document.getElementById("register-section");
const usernameDisplay = document.getElementById("username-display");
const pointsDisplay = document.getElementById("points-display");
const logoutBtn = document.getElementById("logout-btn");
const gameCards = document.querySelectorAll(".game-card:not(.disabled)");
const toast = document.getElementById("toast");

// Funktion: showToast(message, type = "success")
// Zeigt eine kurze Benachrichtigung (Toast) am unteren Rand an. `type` steuert
// die Stil-Klasse (z. B. success/error). Automatisch nach 3s ausblenden.
function showToast(message, type = "success") {
  toast.textContent = message;
  toast.className = `toast show ${type}`;
  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

// Tab Switching
const tabButtons = document.querySelectorAll(".tab-btn");
const authForms = document.querySelectorAll(".auth-form");

tabButtons.forEach(button => {
  button.addEventListener("click", () => {
    const targetTab = button.dataset.tab;

    // Update tab buttons
    tabButtons.forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    // Update forms
    authForms.forEach(form => form.classList.remove("active"));
    if (targetTab === "login") {
      loginSection.classList.add("active");
    } else {
      registerSection.classList.add("active");
    }
  });
});

// Form switch links
const switchFormLinks = document.querySelectorAll(".switch-form");
switchFormLinks.forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const target = link.dataset.target;
    const targetButton = document.querySelector(`.tab-btn[data-tab="${target}"]`);
    if (targetButton) {
      targetButton.click();
    }
  });
});

// Funktion: enableGames()
// Macht die Spielkarten interaktiv (Pointer-Events anschalten, Opazität zurücksetzen).
function enableGames() {
  gameCards.forEach(card => {
    card.style.pointerEvents = "all";
    card.style.opacity = "1";
  });
}

// Funktion: disableGames()
// Deaktiviert die Spielkarten (keine Interaktion möglich) und dimmt sie optisch.
function disableGames() {
  gameCards.forEach(card => {
    card.style.pointerEvents = "none";
    card.style.opacity = "0.6";
  });
}

// Funktion: updateUI(authenticated, userData = null)
// Aktualisiert die Oberfläche abhängig davon, ob der Benutzer angemeldet ist.
// - Bei angemeldet: zeigt Benutzername, Punkte und Logout-Button; blendet das
//   Auth-Formular aus und aktiviert Spielkarten.
// - Bei abgemeldet: setzt UI zurück, zeigt Auth-Bereich und deaktiviert Spiele.
function updateUI(authenticated, userData = null) {
  if (authenticated && userData) {
    // Show user info
    usernameDisplay.textContent = `👤 ${userData.username}`;
    pointsDisplay.textContent = `💰 ${userData.points} Points`;

    // Show logout button
    logoutBtn.style.display = "inline-block";

    // Hide auth section, show welcome
    authSection.style.display = "none";
    welcomeSection.style.display = "block";

    // Enable games
    enableGames();
  } else {
    // Clear user info
    usernameDisplay.textContent = "";
    pointsDisplay.textContent = "";

    // Hide logout button
    logoutBtn.style.display = "none";

    // Show auth section, hide welcome
    authSection.style.display = "block";
    welcomeSection.style.display = "none";

    // Disable games
    disableGames();
  }
}

// Funktion: checkSession()
// Fragt beim Backend die aktuelle Session/Authentifizierung ab und ruft
// `updateUI` mit den erhaltenen Daten auf. Bei Fehlern wird die UI in den
// abgemeldeten Zustand versetzt.
async function checkSession() {
  try {
    const res = await fetch("http://localhost:8000/api/casino/session/", {
      credentials: "include"
    });
    const data = await res.json();

    if (data.authenticated) {
      updateUI(true, data.user);
    } else {
      updateUI(false);
    }
  } catch (err) {
    console.error("Session check error:", err);
    updateUI(false);
  }
}

// Initialer Aufruf: prüft beim Laden, ob bereits eine Session besteht.
checkSession();

// Login-Handler: verarbeitet das Login-Formular, sendet die Daten an das Backend,
// zeigt Rückmeldungen (Toast) und aktualisiert die Session/UI nach Erfolg.
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const submitBtn = e.target.querySelector(".btn-submit");
  const originalText = submitBtn.textContent;
  submitBtn.textContent = "Logging in...";
  submitBtn.disabled = true;

  const formData = Object.fromEntries(new FormData(e.target));

  try {
    const response = await fetch("http://localhost:8000/api/casino/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: "include",
      body: JSON.stringify(formData)
    });

    const data = await response.json();

    if (response.ok) {
      showToast(`Welcome back, ${data.user.username}!`, "success");
      e.target.reset();
      await checkSession();
    } else {
      showToast(data.error || "Invalid credentials", "error");
    }
  } catch (err) {
    showToast("Server error. Please try again.", "error");
    console.error("Login error:", err);
  } finally {
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
  }
});

// Registrierungs-Handler: verarbeitet das Registrierungsformular, sendet die
// Daten an das Backend, zeigt Erfolg/Fehler als Toast und aktualisiert die UI.
document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const submitBtn = e.target.querySelector(".btn-submit");
  const originalText = submitBtn.textContent;
  submitBtn.textContent = "Creating account...";
  submitBtn.disabled = true;

  const formData = Object.fromEntries(new FormData(e.target));

  try {
    const response = await fetch("http://localhost:8000/api/casino/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: "include",
      body: JSON.stringify(formData)
    });

    const data = await response.json();

    if (response.ok) {
      showToast(`Welcome, ${data.user.username}! You received 1000 free points!`, "success");
      e.target.reset();
      await checkSession();
    } else {
      showToast(data.error || "Registration failed", "error");
    }
  } catch (err) {
    showToast("Server error. Please try again.", "error");
    console.error("Registration error:", err);
  } finally {
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
  }
});

// Logout-Handler: sendet eine Logout-Anfrage an das Backend und aktualisiert UI.
logoutBtn.addEventListener("click", async () => {
  const csrftoken = getCookie('csrftoken');

  try {
    const res = await fetch("http://localhost:8000/api/casino/logout/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": csrftoken
      }
    });

    if (res.ok) {
      showToast("Logged out successfully", "success");
      await checkSession();
    } else {
      showToast("Logout failed", "error");
      console.error("Logout failed:", res.status);
    }
  } catch (err) {
    showToast("Server error", "error");
    console.error("Logout error:", err);
  }
});

// Hover-Animation für Spielkarten: visuelles Feedback beim Überfahren mit der Maus.
gameCards.forEach(card => {
  card.addEventListener("mouseenter", () => {
    card.style.transform = "translateY(-10px)";
  });

  card.addEventListener("mouseleave", () => {
    card.style.transform = "translateY(0)";
  });
});

// Klick auf Spielkarten: zeigt optionalen Ladezustand an bevor navigiert wird.
gameCards.forEach(card => {
  const link = card.querySelector("a");
  if (link) {
    link.addEventListener("click", (e) => {
      card.classList.add("loading");
    });
  }
});

// Formulare: Fokus-Effekte für Eingabefelder (leichtes Zoomen des Containers).
const formInputs = document.querySelectorAll(".form-group input");
formInputs.forEach(input => {
  input.addEventListener("focus", () => {
    input.parentElement.style.transform = "scale(1.02)";
    input.parentElement.style.transition = "transform 0.2s ease";
  });

  input.addEventListener("blur", () => {
    input.parentElement.style.transform = "scale(1)";
  });
});

// Tastaturkürzel: z. B. Escape setzt aktive Formulare zurück.
document.addEventListener("keydown", (e) => {
  // Escape key closes any modals or resets form
  if (e.key === "Escape") {
    const activeForm = document.querySelector(".auth-form.active form");
    if (activeForm) {
      activeForm.reset();
    }
  }
});

// UX: Verhindert unbeabsichtigtes Absenden per Enter in Eingabefeldern;
// stattdessen wird der eigentliche Submit-Button ausgelöst.
document.querySelectorAll(".auth-form input").forEach(input => {
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && e.target.type !== "submit") {
      e.preventDefault();
      const form = e.target.closest("form");
      const submitBtn = form.querySelector(".btn-submit");
      submitBtn.click();
    }
  });
});

// Entwickler-Log: Seite ist initialisiert und bereit.
console.log("Student Gambling Site - Ready to play!");
