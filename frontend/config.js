// config.js
(function bootstrapConfig() {
    const runtimeConfig = window.__SPEEDREAD_CONFIG__ || {};

    const normalize = (url) => {
        if (typeof url !== 'string') return '';
        const trimmed = url.trim();
        if (!trimmed) return '';
        return trimmed.replace(/\/$/, '');
    };

    const isLocalhost = ['localhost', '127.0.0.1'].includes(window.location.hostname);
    const fallbackApiBaseUrl = isLocalhost ? 'http://localhost:5000/api' : '/api';

    const configuredApiBaseUrl = normalize(
        runtimeConfig.API_BASE_URL || window.API_BASE_URL || ''
    );

    window.API_BASE_URL = configuredApiBaseUrl || fallbackApiBaseUrl;
})();
