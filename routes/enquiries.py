from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Enquiry, PGListing
import uuid

enquiries_bp = Blueprint('enquiries', __name__)

@enquiries_bp.route('/<pg_id>', methods=['POST'])
@jwt_required()
def create_enquiry(pg_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    pg = PGListing.query.get(pg_id)
    if not pg:
        return jsonify({'success': False, 'error': 'PG not found'}), 404
    
    enquiry = Enquiry(
        id=str(uuid.uuid4()),
        message=data.get('message'),
        tenant_id=user_id,
        owner_id=pg.owner_id,
        pg_listing_id=pg_id,
        status='PENDING'
    )
    
    db.session.add(enquiry)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Enquiry sent successfully',
        'data': {
            'id': enquiry.id,
            'status': enquiry.status
        }
    }), 201
