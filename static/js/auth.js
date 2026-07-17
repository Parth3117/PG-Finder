// Authentication Helper Functions

async function signup(name, email, phone, userType, password) {
    return apiCall('/auth/signup', 'POST', {
        name,
        email,
        phone,
        user_type: userType,
        password
    });
}

async function login(email, password) {
    return apiCall('/auth/login', 'POST', { email, password });
}

async function getProfile() {
    return apiCall('/auth/profile', 'GET');
}

function setAuthToken(token) {
    localStorage.setItem('token', token);
}

function getAuthToken() {
    return localStorage.getItem('token');
}

function isLoggedIn() {
    return !!localStorage.getItem('token');
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

// Update UI based on auth status
function updateAuthUI() {
    const authNav = document.getElementById('authNav');
    const loggedInNav = document.getElementById('loggedInNav');

    if (isLoggedIn()) {
        if (authNav) authNav.style.display = 'none';
        if (loggedInNav) loggedInNav.style.display = 'flex';
    } else {
        if (authNav) authNav.style.display = 'flex';
        if (loggedInNav) loggedInNav.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', updateAuthUI);
