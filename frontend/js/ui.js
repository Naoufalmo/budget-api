// Gestion de l'interface utilisateur
const UI = {
    inactivityTimer: null,
    lastActivityTime: null,
    timerUpdateInterval: null,

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

    startInactivityTimer() {
        // Arrêter les timers existants
        this.stopInactivityTimer();

        // Initialiser le temps de dernière activité
        this.lastActivityTime = Date.now();

        // Mettre à jour l'affichage du timer chaque seconde
        this.timerUpdateInterval = setInterval(() => {
            const timeSinceActivity = Date.now() - this.lastActivityTime;
            const timeRemaining = CONFIG.INACTIVITY_TIMEOUT - timeSinceActivity;

            if (timeRemaining <= 0) {
                // Déconnexion par inactivité
                this.stopInactivityTimer();
                alert('Vous avez été déconnecté pour cause d\'inactivité.');
                Auth.logout();
            } else {
                // Mettre à jour l'affichage
                this.updateTimerDisplay(timeRemaining);
            }
        }, 1000);

        // Écouter les événements d'activité
        this.attachActivityListeners();

        console.log('Timer d\'inactivité démarré');
    },

    stopInactivityTimer() {
        if (this.timerUpdateInterval) {
            clearInterval(this.timerUpdateInterval);
            this.timerUpdateInterval = null;
        }

        if (this.inactivityTimer) {
            clearTimeout(this.inactivityTimer);
            this.inactivityTimer = null;
        }

        this.removeActivityListeners();
    },

    resetInactivityTimer() {
        this.lastActivityTime = Date.now();
        // console.log('🔄 Timer réinitialisé'); // Debug
    },

    // ✅ NOUVEAU : Attacher les listeners d'activité
    attachActivityListeners() {
        // Liste des événements qui comptent comme "activité"
        const activityEvents = [
            'mousedown',    // Click souris
            'mousemove',    // Mouvement souris
            'keydown',      // Touche clavier
            'scroll',       // Scroll
            'touchstart',   // Touch mobile
            'click'         // Click général
        ];

        // Attacher les listeners sur le document
        activityEvents.forEach(event => {
            document.addEventListener(event, this.resetInactivityTimer.bind(this), { passive: true });
        });
    },

    removeActivityListeners() {
        const activityEvents = ['mousedown', 'mousemove', 'keydown', 'scroll', 'touchstart', 'click'];

        activityEvents.forEach(event => {
            document.removeEventListener(event, this.resetInactivityTimer.bind(this));
        });
    },

    // Mettre à jour l'affichage du timer
    updateTimerDisplay(milliseconds) {
        const minutes = Math.floor(milliseconds / 60000);
        const seconds = Math.floor((milliseconds % 60000) / 1000);
        const timerDisplay = document.getElementById('timer-display');

        if (timerDisplay) {
            timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

            // ✅ NOUVEAU : Changer la couleur si moins d'1 minute
            if (minutes === 0 && seconds <= 60) {
                timerDisplay.style.color = '#ef4444'; // Rouge
                timerDisplay.style.fontWeight = 'bold';
            } else {
                timerDisplay.style.color = '';
                timerDisplay.style.fontWeight = '';
            }
        }
    }
};

// Exposer globalement
window.UI = UI;