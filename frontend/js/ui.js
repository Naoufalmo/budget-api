// Gestion de l'interface utilisateur
const UI = {
    // Toggle dark mode
    toggleTheme() {
        document.body.classList.toggle('dark-mode');
        const icon = document.querySelector('.theme-icon');

        if (document.body.classList.contains('dark-mode')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            localStorage.setItem(CONFIG.STORAGE_KEYS.THEME, 'dark');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            localStorage.setItem(CONFIG.STORAGE_KEYS.THEME, 'light');
        }
    },

    // Charger le thème sauvegardé
    loadTheme() {
        const savedTheme = localStorage.getItem(CONFIG.STORAGE_KEYS.THEME);
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-mode');
            const icon = document.querySelector('.theme-icon');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    },

    // Afficher l'alerte financière
    updateFinancialAlert(income, expense) {
        const alertDiv = document.getElementById('financial-alert');
        const alertMessage = alertDiv.querySelector('.alert-message');
        const alertIcon = alertDiv.querySelector('.alert-icon');

        if (income === 0 && expense === 0) {
            alertDiv.style.display = 'none';
            return;
        }

        alertDiv.classList.remove('danger', 'warning', 'success');

        if (expense > income) {
            alertDiv.classList.add('danger');
            alertIcon.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
            alertMessage.textContent = `Attention ! Vos dépenses dépassent vos revenus de ${(expense - income).toFixed(2)} $. Réduisez vos dépenses.`;
        } else if (expense === income) {
            alertDiv.classList.add('warning');
            alertIcon.innerHTML = '<i class="fa-solid fa-bolt"></i>';
            alertMessage.textContent = `Prudence ! Vos dépenses égalent vos revenus. Pensez à économiser.`;
        } else {
            alertDiv.classList.add('success');
            alertIcon.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
            alertMessage.textContent = `Bravo ! Vous économisez ${(income - expense).toFixed(2)} $ ce mois-ci.`;
        }

        alertDiv.style.display = 'flex';
    },

    // Timer de session
    startSessionTimer() {
        if (Auth.sessionTimerInterval) {
            clearInterval(Auth.sessionTimerInterval);
        }

        const loginTime = Date.now();
        localStorage.setItem(CONFIG.STORAGE_KEYS.LOGIN_TIME, loginTime.toString());

        this.updateTimerDisplay(CONFIG.TOKEN_EXPIRY);

        Auth.sessionTimerInterval = setInterval(() => {
            const elapsed = Date.now() - loginTime;
            const remaining = CONFIG.TOKEN_EXPIRY - elapsed;

            if (remaining <= 0) {
                clearInterval(Auth.sessionTimerInterval);
                alert('Votre session a expiré !');
                Auth.logout();
            } else {
                this.updateTimerDisplay(remaining);
            }
        }, 1000); // Mise à jour chaque seconde
    },

    // Mettre à jour l'affichage du timer
    updateTimerDisplay(milliseconds) {
        const minutes = Math.floor(milliseconds / 60000);
        const seconds = Math.floor((milliseconds % 60000) / 1000);
        document.getElementById('timer-display').textContent =
            `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
};

// Exposer globalement
window.UI = UI;