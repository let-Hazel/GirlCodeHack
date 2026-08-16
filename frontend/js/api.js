const API_BASE = 'http://127.0.0.1:5000';

async function api(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        }
    });
    const result = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(result.error || 'Request failed');
    return result;
}

function saveSession(user) {
    localStorage.setItem('skilllinkUser', JSON.stringify(user));
}

function getSession() {
    try { return JSON.parse(localStorage.getItem('skilllinkUser')) || null; }
    catch { return null; }
}

function logout() {
    localStorage.removeItem('skilllinkUser');
    window.location.href = 'login.html';
}
