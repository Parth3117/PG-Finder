// ============================================
// PG FINDER - Authentication Helper Functions
// ============================================

class AuthManager {
  static saveToken(token) {
    localStorage.setItem('token', token);
  }

  static getToken() {
    return localStorage.getItem('token');
  }

  static removeToken() {
    localStorage.removeItem('token');
  }

  static saveUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  static getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  static removeUser() {
    localStorage.removeItem('user');
  }

  static isLoggedIn() {
    return !!this.getToken();
  }

  static logout() {
    this.removeToken();
    this.removeUser();
    window.location.href = '/';
  }

  static async signup(userData) {
    try {
      const response = await AuthAPI.signup(userData);
      
      if (response.token) {
        this.saveToken(response.token);
        this.saveUser(response.user);
        showSuccess('Account created successfully!');
        setTimeout(() => {
          window.location.href = '/search';
        }, 1500);
      } else {
        showError(response.message || 'Signup failed');
      }
    } catch (error) {
      showError('Error during signup: ' + error.message);
    }
  }

  static async login(email, password) {
    try {
      const response = await AuthAPI.login({ email, password });
      
      if (response.token) {
        this.saveToken(response.token);
        this.saveUser(response.user);
        showSuccess('Login successful!');
        setTimeout(() => {
          window.location.href = '/search';
        }, 1500);
      } else {
        showError(response.message || 'Login failed');
      }
    } catch (error) {
      showError('Error during login: ' + error.message);
    }
  }

  static requireLogin() {
    if (!this.isLoggedIn()) {
      showError('Please log in first');
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
      return false;
    }
    return true;
  }
}

// ============================================
// PAGE INITIALIZATION
// ============================================

function initializeAuthUI() {
  const user = AuthManager.getUser();
  const authPlaceholder = document.getElementById('auth-placeholder');
  
  if (authPlaceholder) {
    if (user) {
      authPlaceholder.innerHTML = `
        <div class="nav-buttons">
          <span class="user-info">Welcome, ${user.name}</span>
          <button class="btn btn-secondary" id="logout-btn">Logout</button>
          ${user.user_type === 'OWNER' ? `<a href="/dashboard" class="btn btn-primary">Dashboard</a>` : ''}
        </div>
      `;
      document.getElementById('logout-btn').addEventListener('click', () => {
        AuthManager.logout();
      });
    } else {
      authPlaceholder.innerHTML = `
        <div class="nav-buttons">
          <a href="/login" class="btn btn-secondary">Login</a>
          <a href="/signup" class="btn btn-primary">Sign Up</a>
        </div>
      `;
    }
  }
}

// ============================================
// HANDLE SIGNUP FORM
// ============================================

function handleSignup() {
  const form = document.getElementById('signup-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    const userData = {
      name: formData.get('name'),
      email: formData.get('email'),
      phone: formData.get('phone'),
      password: formData.get('password'),
      user_type: formData.get('user_type'),
    };

    const password2 = formData.get('password2');
    if (userData.password !== password2) {
      showError('Passwords do not match');
      return;
    }

    if (userData.password.length < 6) {
      showError('Password must be at least 6 characters');
      return;
    }

    await AuthManager.signup(userData);
  });
}

// ============================================
// HANDLE LOGIN FORM
// ============================================

function handleLogin() {
  const form = document.getElementById('login-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    const email = formData.get('email');
    const password = formData.get('password');

    await AuthManager.login(email, password);
  });
}

// ============================================
// DOCUMENT READY
// ============================================

document.addEventListener('DOMContentLoaded', () => {
  initializeAuthUI();
  handleSignup();
  handleLogin();
});
