// Gestion de l'authentification
const Auth = {
    token: null,
    currentUser: null,
    isRegisterMode: false,
    sessionTimerInterval: null,

    // Basculer entre Login et Register
    toggleAuthMode() {
        this.isRegisterMode = !this.isRegisterMode;

        const emailInput = document.getElementById('email');
        const authTitle = document.getElementById('auth-title');
        const authButton = document.getElementById('auth-button');
        const toggleText = document.getElementById('toggle-text');
        const toggleLink = document.querySelector('.toggle-auth a');

        if (this.isRegisterMode) {
            emailInput.style.display = 'block';
            authTitle.textContent = 'Inscription';
            authButton.textContent = "S'inscrire";
            toggleText.textContent = 'Déjà un compte ?';
            toggleLink.textContent = 'Se connecter';
        } else {
            emailInput.style.display = 'none';
            authTitle.textContent = 'Connexion';
            authButton.textContent = 'Se connecter';
            toggleText.textContent = 'Pas encore de compte ?';
            toggleLink.textContent = "S'inscrire";
        }
    },

    // Fonction unifiée pour Login OU Register
    async handleAuth() {
        if (this.isRegisterMode) {
            await this.register();
        } else {
            await this.login();
        }
    },

    // Inscription
    async register() {
        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (!email || !username || !password) {
            alert('Veuillez remplir tous les champs');
            return;
        }

        try {
            const response = await fetch(`${CONFIG.API_URL}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, username, password })
            });

            if (!response.ok) {
                const error = await response.json();
                alert(`Erreur: ${error.detail}`);
                return;
            }

            alert('Compte créé avec succès ! Vous pouvez maintenant vous connecter.');
            this.toggleAuthMode();
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';

        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'inscription');
        }
    },

    // Connexion
    async login() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (!username || !password) {
            alert('Veuillez remplir tous les champs');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${CONFIG.API_URL}/api/auth/login`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                alert('Nom d\'utilisateur ou mot de passe incorrect');
                return;
            }

            const data = await response.json();
            this.token = data.access_token;
            this.currentUser = username;

            // Sauvegarder dans localStorage
            localStorage.setItem(CONFIG.STORAGE_KEYS.TOKEN, this.token);
            localStorage.setItem(CONFIG.STORAGE_KEYS.USER, username);

            console.log('Login réussi, username:', username);

            // Afficher le dashboard
            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            document.getElementById('current-username').textContent = username;

            // Charger les données et démarrer le timer
            await Transactions.loadData();
            UI.startSessionTimer();

        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur de connexion');
        }
    },

    // Déconnexion
    logout() {
        if (!confirm('Voulez-vous vraiment vous déconnecter ?')) {
            return;
        }

        // Arrêter le timer
        if (this.sessionTimerInterval) {
            clearInterval(this.sessionTimerInterval);
            this.sessionTimerInterval = null;
        }

        // Réinitialiser
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem(CONFIG.STORAGE_KEYS.TOKEN);
        localStorage.removeItem(CONFIG.STORAGE_KEYS.USER);
        localStorage.removeItem(CONFIG.STORAGE_KEYS.LOGIN_TIME);

        // Vider les champs
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        document.getElementById('email').value = '';
        document.getElementById('new-title').value = '';
        document.getElementById('new-amount').value = '';
        document.getElementById('new-category').value = 'income';

        // Réinitialiser les stats
        document.getElementById('total-income').textContent = '0 $';
        document.getElementById('total-expense').textContent = '0 $';
        document.getElementById('balance').textContent = '0 $';
        document.getElementById('transactions-list').innerHTML = '';
        document.getElementById('current-username').textContent = '';
        document.getElementById('financial-alert').style.display = 'none';
        document.getElementById('timer-display').textContent = '30:00';

        // Afficher auth, cacher dashboard
        document.getElementById('dashboard').style.display = 'none';
        document.getElementById('auth-section').style.display = 'block';

        if (this.isRegisterMode) {
            this.toggleAuthMode();
        }

        console.log('Déconnexion réussie');
    },

    // Restaurer la session
    restoreSession() {
        const savedToken = localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
        const savedUser = localStorage.getItem(CONFIG.STORAGE_KEYS.USER);
        const loginTime = localStorage.getItem(CONFIG.STORAGE_KEYS.LOGIN_TIME);

        if (savedToken && savedUser) {
            // Vérifier si le token n'a pas expiré
            if (loginTime) {
                const elapsed = Date.now() - parseInt(loginTime);
                if (elapsed > CONFIG.TOKEN_EXPIRY) {
                    console.log('Session expirée');
                    this.logout();
                    return;
                }
            }

            console.log('Restauration de la session...');

            this.token = savedToken;
            this.currentUser = savedUser;

            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            document.getElementById('current-username').textContent = savedUser;

            Transactions.loadData().catch(error => {
                console.error('Session expirée');
                this.logout();
            });

            UI.startSessionTimer();
        }
    }
};

// Exposer globalement
window.Auth = Auth;