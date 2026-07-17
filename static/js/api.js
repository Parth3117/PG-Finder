// ============================================
// PG FINDER - API Helper Functions
// ============================================

const API_BASE_URL = '/api';

// ============================================
// AUTHENTICATION ENDPOINTS
// ============================================

class AuthAPI {
  static async signup(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      return await response.json();
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  }

  static async login(credentials) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });
      return await response.json();
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  static async getProfile() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/auth/profile`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return await response.json();
    } catch (error) {
      console.error('Get profile error:', error);
      throw error;
    }
  }

  static async logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
}

// ============================================
// PG LISTING ENDPOINTS
// ============================================

class PGSAPI {
  static async getPGs(params = {}) {
    try {
      const queryString = new URLSearchParams(params).toString();
      const url = `${API_BASE_URL}/pgs${queryString ? '?' + queryString : ''}`;
      const response = await fetch(url);
      return await response.json();
    } catch (error) {
      console.error('Get PGs error:', error);
      throw error;
    }
  }

  static async getPGDetail(pgId) {
    try {
      const response = await fetch(`${API_BASE_URL}/pgs/${pgId}`);
      return await response.json();
    } catch (error) {
      console.error('Get PG detail error:', error);
      throw error;
    }
  }

  static async createPG(pgData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/pgs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(pgData),
      });
      return await response.json();
    } catch (error) {
      console.error('Create PG error:', error);
      throw error;
    }
  }

  static async updatePG(pgId, pgData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/pgs/${pgId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(pgData),
      });
      return await response.json();
    } catch (error) {
      console.error('Update PG error:', error);
      throw error;
    }
  }
}

// ============================================
// REVIEWS ENDPOINTS
// ============================================

class ReviewsAPI {
  static async getReviews(pgId) {
    try {
      const response = await fetch(`${API_BASE_URL}/reviews/${pgId}`);
      return await response.json();
    } catch (error) {
      console.error('Get reviews error:', error);
      throw error;
    }
  }

  static async createReview(pgId, reviewData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/reviews/${pgId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(reviewData),
      });
      return await response.json();
    } catch (error) {
      console.error('Create review error:', error);
      throw error;
    }
  }
}

// ============================================
// FAVORITES ENDPOINTS
// ============================================

class FavoritesAPI {
  static async getFavorites() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/favorites`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return await response.json();
    } catch (error) {
      console.error('Get favorites error:', error);
      throw error;
    }
  }

  static async addFavorite(pgId) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/favorites/${pgId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return await response.json();
    } catch (error) {
      console.error('Add favorite error:', error);
      throw error;
    }
  }

  static async removeFavorite(pgId) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/favorites/${pgId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return await response.json();
    } catch (error) {
      console.error('Remove favorite error:', error);
      throw error;
    }
  }
}

// ============================================
// ENQUIRIES ENDPOINTS
// ============================================

class EnquiriesAPI {
  static async sendEnquiry(pgId, enquiryData) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/enquiries/${pgId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(enquiryData),
      });
      return await response.json();
    } catch (error) {
      console.error('Send enquiry error:', error);
      throw error;
    }
  }

  static async getEnquiries() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
      const response = await fetch(`${API_BASE_URL}/enquiries`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return await response.json();
    } catch (error) {
      console.error('Get enquiries error:', error);
      throw error;
    }
  }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function showError(message) {
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-error';
  alertDiv.textContent = message;
  document.body.prepend(alertDiv);
  setTimeout(() => alertDiv.remove(), 5000);
}

function showSuccess(message) {
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-success';
  alertDiv.textContent = message;
  document.body.prepend(alertDiv);
  setTimeout(() => alertDiv.remove(), 5000);
}

function showLoading(element) {
  element.innerHTML = '<div class="loading"></div>';
}

function isAuthenticated() {
  return !!localStorage.getItem('token');
}

function getToken() {
  return localStorage.getItem('token');
}

function getCurrentUser() {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
}
