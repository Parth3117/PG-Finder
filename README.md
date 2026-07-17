# 🏠 PG Finder - Paying Guest Accommodation Finder

A full-stack web application to search, compare, and book PG/hostel accommodations across India.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![HTML5](https://img.shields.io/badge/HTML5-E34C26)
![CSS3](https://img.shields.io/badge/CSS3-1572B6)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

### For Tenants
- 🔍 **Search & Filter** - Find PGs by city, area, budget, amenities, and more
- ⭐ **Ratings & Reviews** - Read and write reviews from real residents
- ❤️ **Favorites** - Save your favorite PGs for later
- 💬 **Contact Owner** - Send enquiries directly to PG owners
- 📱 **Responsive Design** - Works seamlessly on mobile and desktop
- 🔐 **Secure Authentication** - JWT-based login and signup

### For Owners
- 📝 **List Properties** - Add and manage your PG listings
- 📊 **Dashboard** - View enquiries and manage availability
- ⚙️ **Full Control** - Edit pricing, amenities, and house rules

### General
- ✅ **Verified Listings** - All PGs are verified for authenticity
- 🚫 **No Brokerage** - 100% transparent, no hidden charges
- 🌍 **Multi-City Support** - Support for 25+ cities across India
- 📸 **Photo Gallery** - High-quality images for each PG
- 🗺️ **Location Mapping** - Google Maps integration

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask 3.0
- SQLAlchemy ORM
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-Origin Support)

**Frontend:**
- HTML5
- CSS3 (Responsive Design)
- Vanilla JavaScript (ES6+)
- No external frontend framework (lightweight)

**Database:**
- MySQL or PostgreSQL
- SQLAlchemy Models

**Others:**
- JWT (JSON Web Tokens)
- Bcrypt (Password Hashing)

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL or PostgreSQL
- pip (Python package manager)
- Git
- Virtual Environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Parth3117/pg-finder.git
cd pg-finder
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

#### Option A: MySQL

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE pg_finder;
EXIT;
```

#### Option B: PostgreSQL

```bash
# Create database
psql -U postgres -c "CREATE DATABASE pg_finder;"
```

### 5. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` file with your database credentials:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost/pg_finder
# Or for PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost/pg_finder

# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your_secret_key_here_change_in_production

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here_change_in_production
JWT_ACCESS_TOKEN_EXPIRES=604800

# Server Configuration
DEBUG=True
PORT=5000
HOST=127.0.0.1
```

### 6. Initialize Database

```bash
# Create tables
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Seed Sample Data

```bash
python seed.py
```

This will create:
- 10 PG owner accounts
- 10 realistic PG listings across different cities
- 5 tenant accounts for testing
- Sample reviews and favorites

### 8. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 📁 Project Structure

```
pg-finder/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── seed.py                     # Database seeding script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── README.md                  # This file
│
├── routes/                    # API route handlers
│   ├── __init__.py
│   ├── auth.py               # Authentication endpoints
│   ├── pgs.py                # PG listing endpoints
│   ├── reviews.py            # Review endpoints
│   ├── favorites.py          # Favorite endpoints
│   └── enquiries.py          # Enquiry endpoints
│
├── templates/                # HTML templates
│   ├── index.html            # Landing/home page
│   ├── search.html           # Search and listings
│   ├── pg_detail.html        # PG detail page
│   ├── login.html            # Login page
│   ├── signup.html           # Signup page
│   └── dashboard.html        # User dashboard (TODO)
│
├── static/                   # Static files
│   ├── css/
│   │   ├── style.css         # Main stylesheet
│   │   └── responsive.css    # Responsive design
│   ├── js/
│   │   ├── api.js            # API helper functions
│   │   ├── auth.js           # Authentication helpers
│   │   └── main.js           # Main application logic
│   └── images/               # Static images
│
└── prisma/                   # Prisma migrations (if using PostgreSQL)
    └── migrations/
```

## 🔌 API Endpoints

### Authentication

```http
# Sign up
POST /api/auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "user_type": "TENANT",
  "password": "secure_password"
}

# Login
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}

# Get profile (requires JWT)
GET /api/auth/profile
Authorization: Bearer <JWT_TOKEN>
```

### PG Listings

```http
# Get all PGs with filters
GET /api/pgs?city=Delhi&area=Hauz%20Khas&page=1&limit=10

# Get PG details
GET /api/pgs/{pg_id}
```

### Reviews

```http
# Create review (requires JWT)
POST /api/reviews/{pg_id}
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "rating": 5,
  "comment": "Great place to stay!"
}
```

### Favorites

```http
# Get favorites (requires JWT)
GET /api/favorites
Authorization: Bearer <JWT_TOKEN>

# Add to favorites (requires JWT)
POST /api/favorites/{pg_id}
Authorization: Bearer <JWT_TOKEN>

# Remove from favorites (requires JWT)
DELETE /api/favorites/{pg_id}
Authorization: Bearer <JWT_TOKEN>
```

### Enquiries

```http
# Send enquiry (requires JWT)
POST /api/enquiries/{pg_id}
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "message": "Hi, I'm interested in renting a room. Can you provide more details?"
}
```

## 👤 Test Credentials

After running `seed.py`, you can use these credentials to test:

**Owner Account:**
- Email: `raj@pgfinder.com`
- Password: `password123`
- Type: Owner

**Tenant Account:**
- Email: `tenant1@gmail.com`
- Password: `password123`
- Type: Tenant

## 📊 Sample Data

The seed script creates:

1. **10 PG Listings** across major cities:
   - Delhi (Hauz Khas, Dwarka, North Campus)
   - Noida (Sector 62)
   - Gurgaon (MG Road)
   - Bangalore (Koramangala)
   - Pune (Hinjewadi)
   - Mumbai (Bandra)
   - Hyderabad (Jubilee Hills)
   - Kolkata (Salt Lake)

2. **Realistic Data:**
   - High-quality images from Unsplash
   - Detailed descriptions
   - Multiple amenities and house rules
   - Pricing for different sharing types (single, double, triple)
   - Reviews and ratings
   - Owner contact information

## 🔐 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation
- ✅ Secure password storage
- ✅ Token expiration (7 days)

## 📱 Responsive Design

- ✅ Mobile-first approach
- ✅ Tested on all device sizes
- ✅ Touch-friendly interface
- ✅ Optimized loading times
- ✅ Fluid layouts

## 🚀 Deployment

### Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set DATABASE_URL=your_heroku_database_url
heroku config:set JWT_SECRET_KEY=your_secret_key

# Deploy
git push heroku main

# Run migrations and seed
heroku run python seed.py
```

### AWS EC2

```bash
# 1. Connect to EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 2. Install dependencies
sudo yum install python3 python3-pip mysql

# 3. Clone repository
git clone https://github.com/Parth3117/pg-finder.git
cd pg-finder

# 4. Create virtual environment and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 6. Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check if MySQL is running
mysql -u root -p

# Or for PostgreSQL
psql -U postgres

# Verify DATABASE_URL in .env
```

### JWT Authentication Error

```bash
# Clear browser cookies
# Ctrl+Shift+Delete (or Command+Shift+Delete on Mac)

# Re-login to get a new token
```

### Port Already in Use

```bash
# Run on different port
python app.py --port 5001

# Or kill the process
lsof -ti:5000 | xargs kill -9
```

### Virtual Environment Issues

```bash
# Deactivate and recreate
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 Development Guide

### Adding a New API Endpoint

1. Create a new blueprint in `routes/`
2. Define the route function
3. Register the blueprint in `app.py`
4. Add JWT protection if needed

### Adding a New Database Model

1. Define the model in `models.py`
2. Create migration: `flask db migrate -m "Add new model"`
3. Apply migration: `flask db upgrade`

### Frontend Changes

1. Edit templates in `templates/` folder
2. Add styles in `static/css/`
3. Add JavaScript in `static/js/`
4. No build process needed (vanilla JS)

## 📚 Future Enhancements

- [ ] Payment integration (Razorpay/Stripe)
- [ ] Email notifications
- [ ] SMS alerts
- [ ] Advanced filtering (amenities, distance)
- [ ] Map-based search
- [ ] Image upload functionality
- [ ] Admin dashboard
- [ ] Analytics and reporting
- [ ] Social media login
- [ ] Mobile app (React Native)
- [ ] Video tours
- [ ] Virtual tours with 360° photos

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Parth3117**
- GitHub: [@Parth3117](https://github.com/Parth3117)
- Portfolio: [parth3117.com](https://parth3117.com)

## 📞 Support & Contact

For support, issues, or suggestions:
- Email: support@pgfinder.com
- GitHub Issues: [Create an issue](https://github.com/Parth3117/pg-finder/issues)
- Discussions: [GitHub Discussions](https://github.com/Parth3117/pg-finder/discussions)

## 🙏 Acknowledgments

- Flask documentation and community
- SQLAlchemy ORM
- Unsplash for sample images
- Bootstrap for CSS inspiration
- All contributors and testers

---

**Made with ❤️ by Parth3117**

⭐ If you find this project helpful, please give it a star!
