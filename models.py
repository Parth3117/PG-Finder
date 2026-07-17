from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for tenants and owners"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # TENANT or OWNER
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pg_listings = db.relationship('PGListing', back_populates='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    enquiries = db.relationship('Enquiry', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class PGListing(db.Model):
    """PG Listing model"""
    __tablename__ = 'pg_listings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False, index=True)
    area = db.Column(db.String(100), nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # JSON fields stored as text
    _images = db.Column('images', db.Text, default='[]')
    _amenities = db.Column('amenities', db.Text, default='[]')
    _rules = db.Column('rules', db.Text, default='[]')
    _price_per_room = db.Column('price_per_room', db.Text, default='{}')
    
    owner_name = db.Column(db.String(120), nullable=False)
    owner_phone = db.Column(db.String(20), nullable=False)
    owner_email = db.Column(db.String(120), nullable=False)
    
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='ACTIVE')  # ACTIVE, INACTIVE, DELETED
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', back_populates='pg_listings')
    reviews = db.relationship('Review', back_populates='pg_listing', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', back_populates='pg_listing', cascade='all, delete-orphan')
    enquiries = db.relationship('Enquiry', back_populates='pg_listing', cascade='all, delete-orphan')
    
    # JSON property getters and setters
    @property
    def images(self):
        return json.loads(self._images) if self._images else []
    
    @images.setter
    def images(self, value):
        self._images = json.dumps(value)
    
    @property
    def amenities(self):
        return json.loads(self._amenities) if self._amenities else []
    
    @amenities.setter
    def amenities(self, value):
        self._amenities = json.dumps(value)
    
    @property
    def rules(self):
        return json.loads(self._rules) if self._rules else []
    
    @rules.setter
    def rules(self, value):
        self._rules = json.dumps(value)
    
    @property
    def price_per_room(self):
        return json.loads(self._price_per_room) if self._price_per_room else {}
    
    @price_per_room.setter
    def price_per_room(self, value):
        self._price_per_room = json.dumps(value)
    
    def to_dict(self):
        """Convert PG listing to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'area': self.area,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'images': self.images,
            'amenities': self.amenities,
            'rules': self.rules,
            'price_per_room': self.price_per_room,
            'owner_name': self.owner_name,
            'owner_phone': self.owner_phone,
            'owner_email': self.owner_email,
            'rating': self.rating,
            'review_count': self.review_count,
            'is_verified': self.is_verified,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class Review(db.Model):
    """Review model for PG listings"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pg_id = db.Column(db.String(36), db.ForeignKey('pg_listings.id'), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pg_listing = db.relationship('PGListing', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'pg_id': self.pg_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class Favorite(db.Model):
    """Favorite model for saving PGs"""
    __tablename__ = 'favorites'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    pg_id = db.Column(db.String(36), db.ForeignKey('pg_listings.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicates
    __table_args__ = (db.UniqueConstraint('user_id', 'pg_id', name='uix_user_pg'),)
    
    # Relationships
    user = db.relationship('User', back_populates='favorites')
    pg_listing = db.relationship('PGListing', back_populates='favorites')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pg_id': self.pg_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class Enquiry(db.Model):
    """Enquiry model for contact messages"""
    __tablename__ = 'enquiries'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pg_id = db.Column(db.String(36), db.ForeignKey('pg_listings.id'), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='PENDING')  # PENDING, READ, RESOLVED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pg_listing = db.relationship('PGListing', back_populates='enquiries')
    user = db.relationship('User', back_populates='enquiries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'pg_id': self.pg_id,
            'user_id': self.user_id,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
