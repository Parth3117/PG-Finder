// ============================================
// PG FINDER - Main Application Logic
// ============================================

// ============================================
// SEARCH & FILTER FUNCTIONALITY
// ============================================

class SearchManager {
  static async searchPGs(filters = {}) {
    try {
      showLoading(document.getElementById('listings-grid'));
      const response = await PGSAPI.getPGs(filters);
      
      if (response.pgs) {
        SearchManager.renderListings(response.pgs);
      } else {
        showError(response.message || 'Failed to fetch listings');
      }
    } catch (error) {
      showError('Error fetching listings: ' + error.message);
    }
  }

  static renderListings(listings) {
    const container = document.getElementById('listings-grid');
    if (!container) return;

    if (listings.length === 0) {
      container.innerHTML = '<p class="text-center" style="grid-column: 1 / -1; padding: 2rem;">No PGs found matching your criteria</p>';
      return;
    }

    container.innerHTML = listings.map(pg => `
      <div class="pg-card">
        <img src="${pg.images[0] || 'https://via.placeholder.com/400x300'}" alt="${pg.title}" class="pg-image">
        <div class="pg-content">
          <div class="flex-between">
            <h3 class="pg-title">${pg.title}</h3>
            ${pg.is_verified ? '<span class="verified-badge">✓ Verified</span>' : ''}
          </div>
          <p class="pg-location">📍 ${pg.area}, ${pg.city}</p>
          <p class="pg-price">₹${pg.price_per_room.single || 'N/A'}/month</p>
          
          <div class="pg-rating">
            <span class="rating-stars">★${pg.rating}</span>
            <span>(${pg.review_count} reviews)</span>
          </div>
          
          <div class="pg-amenities">
            ${pg.amenities.slice(0, 3).map(amenity => `<span class="amenity-tag">${amenity}</span>`).join('')}
            ${pg.amenities.length > 3 ? `<span class="amenity-tag">+${pg.amenities.length - 3}</span>` : ''}
          </div>
          
          <div class="pg-footer">
            <button class="btn btn-primary btn-small" onclick="window.location.href='/pg/${pg.id}'">View Details</button>
            <button class="btn btn-secondary btn-small" onclick="toggleFavorite('${pg.id}', this)">❤️</button>
          </div>
        </div>
      </div>
    `).join('');
  }

  static setupFilters() {
    const searchForm = document.getElementById('search-form');
    if (!searchForm) return;

    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(searchForm);
      const filters = Object.fromEntries(formData);
      this.searchPGs(filters);
    });

    // Real-time search as user types
    const inputs = searchForm.querySelectorAll('input, select');
    inputs.forEach(input => {
      input.addEventListener('change', () => {
        const formData = new FormData(searchForm);
        const filters = Object.fromEntries(formData);
        this.searchPGs(filters);
      });
    });
  }
}

// ============================================
// FAVORITES FUNCTIONALITY
// ============================================

async function toggleFavorite(pgId, button) {
  if (!AuthManager.requireLogin()) return;

  try {
    const isFavorited = button.classList.contains('favorited');
    
    if (isFavorited) {
      await FavoritesAPI.removeFavorite(pgId);
      button.classList.remove('favorited');
      button.textContent = '🤍';
      showSuccess('Removed from favorites');
    } else {
      await FavoritesAPI.addFavorite(pgId);
      button.classList.add('favorited');
      button.textContent = '❤️';
      showSuccess('Added to favorites');
    }
  } catch (error) {
    showError('Error updating favorites: ' + error.message);
  }
}

async function loadFavorites() {
  if (!AuthManager.requireLogin()) return;

  try {
    const response = await FavoritesAPI.getFavorites();
    if (response.favorites) {
      const favoriteIds = response.favorites.map(f => f.pg_id);
      localStorage.setItem('favorites', JSON.stringify(favoriteIds));
    }
  } catch (error) {
    console.error('Error loading favorites:', error);
  }
}

function isFavorited(pgId) {
  const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
  return favorites.includes(pgId);
}

// ============================================
// PG DETAIL PAGE
// ============================================

class PGDetailManager {
  static async loadPGDetail(pgId) {
    try {
      showLoading(document.getElementById('pg-detail-container'));
      const response = await PGSAPI.getPGDetail(pgId);
      
      if (response.pg) {
        this.renderPGDetail(response.pg);
        this.setupReviewForm(pgId);
      } else {
        showError(response.message || 'Failed to load PG details');
      }
    } catch (error) {
      showError('Error loading PG details: ' + error.message);
    }
  }

  static renderPGDetail(pg) {
    const container = document.getElementById('pg-detail-container');
    if (!container) return;

    container.innerHTML = `
      <div class="pg-detail">
        <div class="pg-images">
          <img src="${pg.images[0] || 'https://via.placeholder.com/800x500'}" alt="${pg.title}" class="main-image">
          <div class="thumbnail-images">
            ${pg.images.map((img, index) => `
              <img src="${img}" alt="Image ${index + 1}" class="thumbnail" onclick="document.querySelector('.main-image').src='${img}'">
            `).join('')}
          </div>
        </div>
        
        <div class="pg-details-info">
          <div class="flex-between">
            <h1>${pg.title}</h1>
            <button class="btn-icon" onclick="toggleFavorite('${pg.id}', this)">${isFavorited(pg.id) ? '❤️' : '🤍'}</button>
          </div>
          
          <p class="pg-location">📍 ${pg.address}, ${pg.area}, ${pg.city}</p>
          
          <div class="pg-rating-detail">
            <span class="stars">★ ${pg.rating}/5</span>
            <span class="reviews">(${pg.review_count} reviews)</span>
            ${pg.is_verified ? '<span class="verified-badge">✓ Verified</span>' : ''}
          </div>
          
          <div class="price-section">
            <h2>Pricing</h2>
            <div class="price-grid">
              <div class="price-item">
                <span class="label">Single Room:</span>
                <span class="price">₹${pg.price_per_room.single || 'N/A'}/month</span>
              </div>
              <div class="price-item">
                <span class="label">Double Sharing:</span>
                <span class="price">₹${pg.price_per_room.double || 'N/A'}/month</span>
              </div>
              <div class="price-item">
                <span class="label">Triple Sharing:</span>
                <span class="price">₹${pg.price_per_room.triple || 'N/A'}/month</span>
              </div>
            </div>
          </div>
          
          <div class="description-section">
            <h2>Description</h2>
            <p>${pg.description}</p>
          </div>
          
          <div class="amenities-section">
            <h2>Amenities</h2>
            <div class="amenity-list">
              ${pg.amenities.map(amenity => `<span class="amenity-badge">✓ ${amenity}</span>`).join('')}
            </div>
          </div>
          
          <div class="rules-section">
            <h2>House Rules</h2>
            <ul class="rules-list">
              ${pg.rules.map(rule => `<li>• ${rule}</li>`).join('')}
            </ul>
          </div>
          
          <div class="contact-section">
            <h2>Contact Owner</h2>
            <p><strong>${pg.owner_name}</strong></p>
            <p>📞 ${pg.owner_phone}</p>
            <p>📧 ${pg.owner_email}</p>
            <button class="btn btn-primary btn-block" onclick="showEnquiryForm('${pg.id}')">Send Enquiry</button>
          </div>
        </div>
      </div>
      
      <div class="reviews-section">
        <h2>Reviews</h2>
        <div id="reviews-container"></div>
        ${AuthManager.isLoggedIn() ? `<div id="review-form-container"></div>` : '<p>Please <a href="/login">login</a> to write a review</p>'}
      </div>
    `;
    
    this.loadReviews(pg.id);
  }

  static async loadReviews(pgId) {
    try {
      const response = await ReviewsAPI.getReviews(pgId);
      const container = document.getElementById('reviews-container');
      
      if (response.reviews && response.reviews.length > 0) {
        container.innerHTML = response.reviews.map(review => `
          <div class="review-item">
            <div class="review-header">
              <strong>${review.user_name || 'Anonymous'}</strong>
              <span class="stars">★ ${review.rating}/5</span>
            </div>
            <p>${review.comment}</p>
            <small>${new Date(review.created_at).toLocaleDateString()}</small>
          </div>
        `).join('');
      } else {
        container.innerHTML = '<p>No reviews yet</p>';
      }
    } catch (error) {
      console.error('Error loading reviews:', error);
    }
  }

  static setupReviewForm(pgId) {
    if (!AuthManager.isLoggedIn()) return;

    const container = document.getElementById('review-form-container');
    if (!container) return;

    container.innerHTML = `
      <div class="review-form">
        <h3>Write a Review</h3>
        <form id="review-form">
          <div class="form-group">
            <label for="rating">Rating</label>
            <select id="rating" name="rating" required>
              <option value="">Select rating</option>
              <option value="5">5 - Excellent</option>
              <option value="4">4 - Good</option>
              <option value="3">3 - Average</option>
              <option value="2">2 - Poor</option>
              <option value="1">1 - Very Poor</option>
            </select>
          </div>
          <div class="form-group">
            <label for="comment">Comment</label>
            <textarea id="comment" name="comment" required placeholder="Share your experience..."></textarea>
          </div>
          <button type="submit" class="btn btn-primary btn-block">Submit Review</button>
        </form>
      </div>
    `;

    document.getElementById('review-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const reviewData = {
        rating: parseInt(formData.get('rating')),
        comment: formData.get('comment'),
      };

      try {
        const response = await ReviewsAPI.createReview(pgId, reviewData);
        if (response.review) {
          showSuccess('Review submitted successfully!');
          this.loadReviews(pgId);
          e.target.reset();
        } else {
          showError(response.message || 'Failed to submit review');
        }
      } catch (error) {
        showError('Error submitting review: ' + error.message);
      }
    });
  }
}

// ============================================
// ENQUIRY FUNCTIONALITY
// ============================================

function showEnquiryForm(pgId) {
  if (!AuthManager.requireLogin()) return;

  const modal = document.createElement('div');
  modal.className = 'modal active';
  modal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">Send Enquiry</h2>
        <button class="modal-close" onclick="this.closest('.modal').remove()">✕</button>
      </div>
      <form id="enquiry-form" class="enquiry-form">
        <div class="form-group">
          <label for="enquiry-message">Message</label>
          <textarea id="enquiry-message" name="message" required placeholder="Hi, I'm interested in this PG. Can you provide more details?"></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-block">Send Enquiry</button>
      </form>
    </div>
  `;
  document.body.appendChild(modal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.remove();
  });

  document.getElementById('enquiry-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const enquiryData = {
      message: formData.get('message'),
    };

    try {
      const response = await EnquiriesAPI.sendEnquiry(pgId, enquiryData);
      if (response.enquiry) {
        showSuccess('Enquiry sent successfully!');
        modal.remove();
      } else {
        showError(response.message || 'Failed to send enquiry');
      }
    } catch (error) {
      showError('Error sending enquiry: ' + error.message);
    }
  });
}

// ============================================
// PAGE INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
  // Initialize search on search page
  if (document.getElementById('search-form')) {
    SearchManager.setupFilters();
    SearchManager.searchPGs();
  }

  // Initialize PG detail page
  const pgId = document.body.dataset.pgId;
  if (pgId) {
    PGDetailManager.loadPGDetail(pgId);
  }

  // Load favorites if user is logged in
  if (AuthManager.isLoggedIn()) {
    loadFavorites();
  }
});
