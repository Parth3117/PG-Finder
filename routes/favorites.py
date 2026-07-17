from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Favorite, PGListing
import uuid

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': fav.id,
            'pg': {
                'id': fav.pg_listing.id,
                'title': fav.pg_listing.title,
                'city': fav.pg_listing.city,
                'area': fav.pg_listing.area,
                'images': fav.pg_listing.images,
                'rating': fav.pg_listing.rating,
                'review_count': fav.pg_listing.review_count,
                'price_per_room': fav.pg_listing.price_per_room
            }
        } for fav in favorites]
    }), 200

@favorites_bp.route('/<pg_id>', methods=['POST'])
@jwt_required()
def add_favorite(pg_id):
    user_id = get_jwt_identity()
    
    pg = PGListing.query.get(pg_id)
    if not pg:
        return jsonify({'success': False, 'error': 'PG not found'}), 404
    
    existing = Favorite.query.filter_by(user_id=user_id, pg_listing_id=pg_id).first()
    if existing:
        return jsonify({'success': False, 'error': 'Already in favorites'}), 409
    
    favorite = Favorite(
        id=str(uuid.uuid4()),
        user_id=user_id,
        pg_listing_id=pg_id
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Added to favorites'
    }), 201

@favorites_bp.route('/<pg_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(pg_id):
    user_id = get_jwt_identity()
    
    favorite = Favorite.query.filter_by(user_id=user_id, pg_listing_id=pg_id).first()
    if not favorite:
        return jsonify({'success': False, 'error': 'Not in favorites'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Removed from favorites'
    }), 200
