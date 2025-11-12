// Configuration globale de l'application
const CONFIG = {
    API_URL: 'http://localhost:8000',
    INACTIVITY_TIMEOUT: 30 * 1000, // 5 minutes en millisecondes
    STORAGE_KEYS: {
        TOKEN: 'token',
        USER: 'currentUser',
        LOGIN_TIME: 'loginTime',
        THEME: 'theme'
    }
};

// Export pour les autres modules
window.CONFIG = CONFIG;