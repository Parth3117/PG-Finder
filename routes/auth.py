from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from models import User
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'error': 'User already exists'}), 409
    
    user = User(
        id=str(uuid.uuid4()),
        email=data['email'],
        name=data['name'],
        user_type=data.get('user_type', 'TENANT'),
        phone=data.get('phone')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'message': 'User created successfully',
        'token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'user_type': user.user_type
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'user_type': user.user_type
        }
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'phone': user.phone,
            'user_type': user.user_type,
            'avatar': user.avatar
        }
    }), 200
