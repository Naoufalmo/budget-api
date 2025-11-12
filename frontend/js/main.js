// Point d'entrée principal de l'application

// Fonctions globales pour les onclick dans le HTML
function toggleAuthMode() {
    Auth.toggleAuthMode();
}

function handleAuth() {
    Auth.handleAuth();
}

function logout() {
    Auth.logout();
}

function toggleTheme() {
    UI.toggleTheme();
}

function createTransaction() {
    Transactions.createTransaction();
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Charger le thème
    UI.loadTheme();

    // Restaurer la session si elle existe
    Auth.restoreSession();

    // Gérer la touche Entrée pour se connecter
    const passwordInput = document.getElementById('password');
    const usernameInput = document.getElementById('username');

    if (passwordInput) {
        passwordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleAuth();
        });
    }

    if (usernameInput) {
        usernameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleAuth();
        });
    }

    console.log('✅ Application initialisée');
});