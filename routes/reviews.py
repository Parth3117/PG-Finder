from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Review, PGListing
import uuid

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/<pg_id>', methods=['POST'])
@jwt_required()
def create_review(pg_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    pg = PGListing.query.get(pg_id)
    if not pg:
        return jsonify({'success': False, 'error': 'PG not found'}), 404
    
    existing_review = Review.query.filter_by(user_id=user_id, pg_listing_id=pg_id).first()
    if existing_review:
        return jsonify({'success': False, 'error': 'You already reviewed this PG'}), 409
    
    review = Review(
        id=str(uuid.uuid4()),
        rating=data.get('rating'),
        comment=data.get('comment'),
        user_id=user_id,
        pg_listing_id=pg_id
    )
    
    db.session.add(review)
    
    all_reviews = Review.query.filter_by(pg_listing_id=pg_id).all()
    total_rating = sum(r.rating for r in all_reviews) + review.rating
    pg.rating = total_rating / (len(all_reviews) + 1)
    pg.review_count = len(all_reviews) + 1
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Review created successfully',
        'data': {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment
        }
    }), 201
