from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///pg_finder.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key_change_in_production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Flask Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_change_in_production')
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

# Initialize Extensions
from models import db
db.init_app(app)

jwt = JWTManager(app)
CORS(app)

# Register Blueprints
from routes.auth import auth_bp
from routes.pgs import pgs_bp
from routes.reviews import reviews_bp
from routes.favorites import favorites_bp
from routes.enquiries import enquiries_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(pgs_bp, url_prefix='/api/pgs')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
app.register_blueprint(enquiries_bp, url_prefix='/api/enquiries')

# Frontend Routes
@app.route('/')
def index():
    """Landing/Home page"""
    return render_template('index.html')

@app.route('/search')
def search():
    """Search and listings page"""
    return render_template('search.html')

@app.route('/pg/<pg_id>')
def pg_detail(pg_id):
    """PG detail page"""
    return render_template('pg_detail.html', pg_id=pg_id)

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/signup')
def signup():
    """Signup page"""
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500

@app.errorhandler(401)
def unauthorized_error(error):
    """Handle 401 errors"""
    return jsonify({'message': 'Unauthorized access'}), 401

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'PG Finder API is running'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    app.run(host=host, port=port, debug=app.config['DEBUG'])
