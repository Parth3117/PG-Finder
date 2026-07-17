from flask import Blueprint, request, jsonify
from app import db
from models import PGListing, User
import uuid

pgs_bp = Blueprint('pgs', __name__)

@pgs_bp.route('', methods=['GET'])
def get_pgs():
    city = request.args.get('city')
    area = request.args.get('area')
    min_budget = request.args.get('min_budget', type=int)
    max_budget = request.args.get('max_budget', type=int)
    limit = request.args.get('limit', 10, type=int)
    page = request.args.get('page', 1, type=int)
    
    query = PGListing.query.filter_by(status='ACTIVE')
    
    if city:
        query = query.filter(PGListing.city.ilike(f'%{city}%'))
    if area:
        query = query.filter(PGListing.area.ilike(f'%{area}%'))
    
    total = query.count()
    pgs = query.limit(limit).offset((page - 1) * limit).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': pg.id,
            'title': pg.title,
            'description': pg.description,
            'city': pg.city,
            'area': pg.area,
            'images': pg.images,
            'amenities': pg.amenities,
            'price_per_room': pg.price_per_room,
            'rating': pg.rating,
            'review_count': pg.review_count,
            'owner': {
                'id': pg.owner.id,
                'name': pg.owner.name,
                'phone': pg.owner.phone,
                'email': pg.owner.email
            }
        } for pg in pgs],
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit
        }
    }), 200

@pgs_bp.route('/<pg_id>', methods=['GET'])
def get_pg(pg_id):
    pg = PGListing.query.get(pg_id)
    
    if not pg:
        return jsonify({'success': False, 'error': 'PG not found'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': pg.id,
            'title': pg.title,
            'description': pg.description,
            'address': pg.address,
            'city': pg.city,
            'area': pg.area,
            'latitude': pg.latitude,
            'longitude': pg.longitude,
            'images': pg.images,
            'amenities': pg.amenities,
            'rules': pg.rules,
            'price_per_room': pg.price_per_room,
            'rating': pg.rating,
            'review_count': pg.review_count,
            'is_verified': pg.is_verified,
            'owner': {
                'id': pg.owner.id,
                'name': pg.owner.name,
                'phone': pg.owner.phone,
                'email': pg.owner.email,
                'avatar': pg.owner.avatar
            },
            'reviews': [{
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'user': {
                    'name': review.user.name,
                    'avatar': review.user.avatar
                },
                'created_at': review.created_at.isoformat()
            } for review in pg.reviews]
        }
    }), 200
