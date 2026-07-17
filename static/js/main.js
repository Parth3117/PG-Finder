// Main Application Logic

// Format price to Indian currency
function formatPrice(price) {
    return '₹' + price.toLocaleString('en-IN');
}

// Load featured PGs on home page
async function loadFeaturedPGs() {
    const featuredContainer = document.getElementById('featuredPGs');
    if (!featuredContainer) return;

    try {
        const result = await getPGs({ limit: 6 });
        if (result.success) {
            featuredContainer.innerHTML = result.data.map(pg => `
                <div class="pg-card">
                    <div class="pg-image">
                        <img src="${pg.images[0] || 'https://via.placeholder.com/300x200'}" alt="${pg.title}">
                        ${pg.rating >= 4.5 ? `<span class="rating-badge">⭐ ${pg.rating}</span>` : ''}
                    </div>
                    <div class="pg-info">
                        <h3>${pg.title}</h3>
                        <p class="location">📍 ${pg.area}, ${pg.city}</p>
                        <p class="price">From ${formatPrice(Math.min(...Object.values(pg.price_per_room)))}/month</p>
                        <div class="amenities-preview">
                            ${pg.amenities.slice(0, 3).map(a => `<span class="amenity-tag">${a}</span>`).join('')}
                        </div>
                        <div class="pg-footer">
                            <span class="reviews">★ ${pg.rating} (${pg.review_count} reviews)</span>
                            <a href="/pg/${pg.id}" class="btn-secondary">View</a>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading featured PGs:', error);
    }
}

// Search PGs from hero
function searchPGs() {
    const city = document.getElementById('searchCity')?.value || '';
    const budget = document.getElementById('searchBudget')?.value || '';
    
    const params = new URLSearchParams();
    if (city) params.append('city', city);
    if (budget) params.append('budget', budget);
    
    window.location.href = `/search?${params}`;
}

// Mobile menu toggle
const hamburger = document.getElementById('hamburger');
if (hamburger) {
    hamburger.addEventListener('click', () => {
        const navMenu = document.querySelector('.nav-menu');
        navMenu?.classList.toggle('active');
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadFeaturedPGs();
    updateAuthUI();
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
