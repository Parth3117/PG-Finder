// API Helper Functions

const API_BASE = 'http://localhost:5000/api';

async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    const token = localStorage.getItem('token');
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function getPGs(filters = {}) {
    const params = new URLSearchParams();
    if (filters.city) params.append('city', filters.city);
    if (filters.area) params.append('area', filters.area);
    if (filters.page) params.append('page', filters.page);
    if (filters.limit) params.append('limit', filters.limit);
    
    return apiCall(`/pgs?${params}`);
}

async function getPGDetail(pgId) {
    return apiCall(`/pgs/${pgId}`);
}

async function addReview(pgId, rating, comment) {
    return apiCall(`/reviews/${pgId}`, 'POST', { rating, comment });
}

async function addFavorite(pgId) {
    return apiCall(`/favorites/${pgId}`, 'POST');
}

async function removeFavorite(pgId) {
    return apiCall(`/favorites/${pgId}`, 'DELETE');
}

async function getFavorites() {
    return apiCall('/favorites');
}

async function sendEnquiry(pgId, message) {
    return apiCall(`/enquiries/${pgId}`, 'POST', { message });
}
