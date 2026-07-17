from app import app, db
from models import User, PGListing
import uuid
import json
from datetime import datetime

SAMPLE_PGS = [
    {
        'title': 'Cozy PG near IIT Delhi',
        'description': 'Spacious rooms with excellent ventilation. Located in Hauz Khas village with easy metro access. WiFi, AC, and daily breakfast included. Perfect for students and young professionals.',
        'address': '123 Hauz Khas Village',
        'city': 'Delhi',
        'area': 'Hauz Khas',
        'latitude': 28.5355,
        'longitude': 77.1962,
        'images': ['https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800', 'https://images.unsplash.com/photo-1554995207-c18231b6ce48?w=800'],
        'amenities': ['WiFi', 'AC', 'Breakfast', 'Laundry', 'Parking', 'CCTV'],
        'rules': ['No smoking', 'Quiet hours after 10 PM', 'No guests after 9 PM'],
        'price_per_room': {'single': 12000, 'double': 8000, 'triple': 6000},
        'owner_name': 'Raj Kumar',
        'owner_phone': '9876543210',
        'owner_email': 'raj@pgfinder.com',
        'rating': 4.5,
        'review_count': 24,
        'is_verified': True,
    },
    {
        'title': 'Modern PG in Sector 62, Noida',
        'description': 'Brand new furnished rooms with attached balconies. Near Infosys and TCS offices. Premium amenities including gym and study room. Ideal for IT professionals.',
        'address': '456 Sector 62',
        'city': 'Noida',
        'area': 'Sector 62',
        'latitude': 28.5744,
        'longitude': 77.3639,
        'images': ['https://images.unsplash.com/photo-1584622181563-430f63602d4b?w=800', 'https://images.unsplash.com/photo-1567521464027-f127ff144326?w=800'],
        'amenities': ['WiFi', 'AC', 'Gym', 'Study Room', 'Dinner included', 'Power Backup'],
        'rules': ['Professional environment', 'No loud music', 'Vegetarian food only'],
        'price_per_room': {'single': 15000, 'double': 10000, 'triple': 7000},
        'owner_name': 'Priya Singh',
        'owner_phone': '9876543211',
        'owner_email': 'priya@pgfinder.com',
        'rating': 4.8,
        'review_count': 35,
        'is_verified': True,
    },
    {
        'title': 'Budget-friendly PG in Dwarka',
        'description': 'Affordable and clean rooms. Walking distance from Dwarka metro. Basic amenities at budget prices. Great for students on a tight budget.',
        'address': '789 Dwarka Sector 7',
        'city': 'Delhi',
        'area': 'Dwarka',
        'latitude': 28.5894,
        'longitude': 77.0461,
        'images': ['https://images.unsplash.com/photo-1555995362-d0fbe4e0a9a9?w=800', 'https://images.unsplash.com/photo-1591825730876-98f5c25dc7f1?w=800'],
        'amenities': ['WiFi', 'Breakfast', 'Laundry', 'Common TV'],
        'rules': ['Student friendly', 'No pets', 'Checkout by 11 AM'],
        'price_per_room': {'single': 6000, 'double': 4500, 'triple': 3500},
        'owner_name': 'Mohammad Ahmed',
        'owner_phone': '9876543212',
        'owner_email': 'ahmed@pgfinder.com',
        'rating': 4.2,
        'review_count': 18,
        'is_verified': False,
    },
    {
        'title': 'Premium PG in Gurgaon - MG Road',
        'description': 'Luxury furnished rooms with housekeeping. Located on MG Road with easy access to all offices. Includes laundry and meals. Perfect for executives.',
        'address': '321 MG Road',
        'city': 'Gurgaon',
        'area': 'MG Road',
        'latitude': 28.4595,
        'longitude': 77.0427,
        'images': ['https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800', 'https://images.unsplash.com/photo-1470115716159-e389f8712fda?w=800'],
        'amenities': ['WiFi', 'AC', 'Housekeeping', 'Gym', 'Dining', 'Parking'],
        'rules': ['Professional only', 'No visitors without permission', 'Smoking on terrace only'],
        'price_per_room': {'single': 18000, 'double': 12000, 'triple': 9000},
        'owner_name': 'Vikram Patel',
        'owner_phone': '9876543213',
        'owner_email': 'vikram@pgfinder.com',
        'rating': 4.9,
        'review_count': 42,
        'is_verified': True,
    },
    {
        'title': 'Co-ed PG near Delhi University',
        'description': 'Vibrant community with students from all across India. Regular events and activities. Fully furnished with modern amenities. Great for social butterflies.',
        'address': '654 North Campus Road',
        'city': 'Delhi',
        'area': 'North Campus',
        'latitude': 28.7041,
        'longitude': 77.1929,
        'images': ['https://images.unsplash.com/photo-1503672260-2540fca44550?w=800', 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=800'],
        'amenities': ['WiFi', 'Breakfast', 'Common Kitchen', 'Gaming Area', 'Study Room'],
        'rules': ['Co-ed friendly', 'Respect everyone', 'Shared responsibilities'],
        'price_per_room': {'single': 7000, 'double': 5000, 'triple': 3500},
        'owner_name': 'Neha Sharma',
        'owner_phone': '9876543214',
        'owner_email': 'neha@pgfinder.com',
        'rating': 4.6,
        'review_count': 28,
        'is_verified': True,
    },
    {
        'title': 'Girls-only PG in Bangalore - Koramangala',
        'description': 'Safe and secure girls-only PG. Located in the heart of Koramangala. 24/7 security with CCTV. Includes all meals and housekeeping. Women only policy.',
        'address': '987 Koramangala 1st Block',
        'city': 'Bangalore',
        'area': 'Koramangala',
        'latitude': 12.9352,
        'longitude': 77.6245,
        'images': ['https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800', 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800'],
        'amenities': ['WiFi', 'AC', 'All Meals', 'Housekeeping', 'CCTV', 'Security Guard'],
        'rules': ['Girls only', 'No smoking', 'Alcohol prohibited', 'Guest policy strict'],
        'price_per_room': {'single': 14000, 'double': 10000, 'triple': 7500},
        'owner_name': 'Divya Reddy',
        'owner_phone': '9876543215',
        'owner_email': 'divya@pgfinder.com',
        'rating': 4.7,
        'review_count': 31,
        'is_verified': True,
    },
    {
        'title': 'PG in Pune - Hinjewadi IT Park',
        'description': 'Perfect for IT professionals. Located near Hinjewadi IT Park. Shuttle service available. Modern furnished rooms with all amenities. Company cab drop provided.',
        'address': '111 Hinjewadi Phase 1',
        'city': 'Pune',
        'area': 'Hinjewadi',
        'latitude': 18.5912,
        'longitude': 73.8235,
        'images': ['https://images.unsplash.com/photo-1523217311519-3580a3e6301d?w=800', 'https://images.unsplash.com/photo-1547394765-185342881546?w=800'],
        'amenities': ['WiFi', 'AC', 'Shuttle', 'Gym', 'Dinner', 'Power Backup'],
        'rules': ['Professional environment', 'Quiet hours 10 PM - 8 AM', 'Smoking area available'],
        'price_per_room': {'single': 11000, 'double': 7500, 'triple': 5500},
        'owner_name': 'Sanjay Desai',
        'owner_phone': '9876543216',
        'owner_email': 'sanjay@pgfinder.com',
        'rating': 4.4,
        'review_count': 22,
        'is_verified': True,
    },
    {
        'title': 'Hostel-style PG in Mumbai - Bandra',
        'description': 'Affordable hostel-style accommodation. Great social atmosphere. Near Bandra station. Mix of single and shared rooms available. Perfect for backpackers.',
        'address': '222 Linking Road',
        'city': 'Mumbai',
        'area': 'Bandra',
        'latitude': 19.0596,
        'longitude': 72.8295,
        'images': ['https://images.unsplash.com/photo-1487730116645-74489c95b41b?w=800', 'https://images.unsplash.com/photo-1469022563149-aa64dbd37dce?w=800'],
        'amenities': ['WiFi', 'Common Kitchen', 'Breakfast', 'Rooftop area', 'Laundry'],
        'rules': ['Social environment', 'Shared responsibilities', 'Keep it clean'],
        'price_per_room': {'single': 10000, 'double': 6500, 'triple': 4500},
        'owner_name': 'Arjun Menon',
        'owner_phone': '9876543217',
        'owner_email': 'arjun@pgfinder.com',
        'rating': 4.3,
        'review_count': 26,
        'is_verified': False,
    },
    {
        'title': 'Executive PG in Hyderabad - Jubilee Hills',
        'description': 'High-end PG for professionals. Located in premium Jubilee Hills. Fully furnished with elegant interiors. Premium meals included. Concierge service available.',
        'address': '333 Jubilee Hills Road 55',
        'city': 'Hyderabad',
        'area': 'Jubilee Hills',
        'latitude': 17.3850,
        'longitude': 78.3967,
        'images': ['https://images.unsplash.com/photo-1522708519590-d0f8c9c3ebef?w=800', 'https://images.unsplash.com/photo-1502672260-481851714409?w=800'],
        'amenities': ['WiFi', 'AC', 'Premium Meals', 'Concierge', 'Parking', 'Laundry'],
        'rules': ['Professional only', 'No pets', 'Formal dress code for common areas'],
        'price_per_room': {'single': 16000, 'double': 11000, 'triple': 8000},
        'owner_name': 'Rahul Sharma',
        'owner_phone': '9876543218',
        'owner_email': 'rahul@pgfinder.com',
        'rating': 4.8,
        'review_count': 39,
        'is_verified': True,
    },
    {
        'title': 'Student-friendly PG in Kolkata - Salt Lake',
        'description': 'Spacious and affordable rooms. Perfect for students and young professionals. Walking distance from shopping mall and metro. Community atmosphere.',
        'address': '444 Salt Lake City Sector V',
        'city': 'Kolkata',
        'area': 'Salt Lake',
        'latitude': 22.5432,
        'longitude': 88.4224,
        'images': ['https://images.unsplash.com/photo-1522251650684-ab0ceae89b0f?w=800', 'https://images.unsplash.com/photo-1557672172-298e090d0f80?w=800'],
        'amenities': ['WiFi', 'Breakfast', 'Study Area', 'Common TV', 'Laundry'],
        'rules': ['Student friendly', 'No smoking inside', 'Keep noise low'],
        'price_per_room': {'single': 5500, 'double': 4000, 'triple': 3000},
        'owner_name': 'Ananya Das',
        'owner_phone': '9876543219',
        'owner_email': 'ananya@pgfinder.com',
        'rating': 4.1,
        'review_count': 16,
        'is_verified': True,
    },
]

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        print('\n🌱 Starting database seed...\n')
        
        try:
            # Create all tables
            db.create_all()
            print('✅ Database tables created')
            
            # Check if data already exists
            existing_pgs = PGListing.query.count()
            if existing_pgs > 0:
                print(f'\n⚠️  Database already contains {existing_pgs} PG listings')
                response = input('Do you want to clear and reseed? (y/n): ').lower()
                if response != 'y':
                    print('Exiting without seeding.')
                    return
                
                # Clear existing data
                db.session.query(PGListing).delete()
                db.session.query(User).delete()
                db.session.commit()
                print('🧹 Cleared existing data')
            
            # Create owners
            owners = []
            print('\n👥 Creating owner accounts...')
            for i, pg_data in enumerate(SAMPLE_PGS):
                owner = User(
                    id=str(uuid.uuid4()),
                    email=pg_data['owner_email'],
                    name=pg_data['owner_name'],
                    phone=pg_data['owner_phone'],
                    user_type='OWNER'
                )
                owner.set_password('password123')
                owners.append(owner)
                db.session.add(owner)
            
            db.session.commit()
            print(f'✅ Created {len(owners)} owner accounts')
            
            # Create PG listings
            print('\n🏠 Creating PG listings...')
            for i, pg_data in enumerate(SAMPLE_PGS):
                pg = PGListing(
                    id=str(uuid.uuid4()),
                    title=pg_data['title'],
                    description=pg_data['description'],
                    address=pg_data['address'],
                    city=pg_data['city'],
                    area=pg_data['area'],
                    latitude=pg_data['latitude'],
                    longitude=pg_data['longitude'],
                    images=pg_data['images'],
                    amenities=pg_data['amenities'],
                    rules=pg_data['rules'],
                    price_per_room=pg_data['price_per_room'],
                    owner_name=pg_data['owner_name'],
                    owner_phone=pg_data['owner_phone'],
                    owner_email=pg_data['owner_email'],
                    rating=pg_data['rating'],
                    review_count=pg_data['review_count'],
                    is_verified=pg_data['is_verified'],
                    status='ACTIVE',
                    owner_id=owners[i].id
                )
                db.session.add(pg)
            
            db.session.commit()
            print(f'✅ Created {len(SAMPLE_PGS)} PG listings')
            
            # Create tenants
            print('\n👤 Creating tenant accounts...')
            tenants = []
            for i in range(5):
                tenant = User(
                    id=str(uuid.uuid4()),
                    email=f'tenant{i+1}@gmail.com',
                    name=f'Tenant {i+1}',
                    phone=f'9000000{i}00',
                    user_type='TENANT'
                )
                tenant.set_password('password123')
                tenants.append(tenant)
                db.session.add(tenant)
            
            db.session.commit()
            print(f'✅ Created {len(tenants)} tenant accounts')
            
            print('\n' + '='*60)
            print('📊 SEEDING COMPLETED SUCCESSFULLY!')
            print('='*60)
            print('\n🔐 Test Credentials:')
            print('\n  Owner Account:')
            print('  Email: raj@pgfinder.com')
            print('  Password: password123')
            print('\n  Tenant Account:')
            print('  Email: tenant1@gmail.com')
            print('  Password: password123')
            print('\n' + '='*60 + '\n')
            
        except Exception as e:
            print(f'\n❌ Error during seeding: {str(e)}')
            db.session.rollback()
            raise

if __name__ == '__main__':
    seed_database()
