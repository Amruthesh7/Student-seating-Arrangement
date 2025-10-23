#!/usr/bin/env python3
"""
Startup script for production deployment
"""

import os
from app import app, db

def initialize_database():
    """Initialize database tables"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if we have any data
            from app import Student, Room
            student_count = Student.query.count()
            room_count = Room.query.count()
            print(f"📊 Database status: {student_count} students, {room_count} rooms")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            return False
    return True

if __name__ == "__main__":
    print("🚀 Starting Student Seating Arrangement Portal...")
    
    # Initialize database
    if initialize_database():
        print("✅ Database initialized successfully")
    else:
        print("❌ Database initialization failed")
    
    # Get port from environment
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Starting server on port {port}")
    
    # Start the application
    app.run(host='0.0.0.0', port=port, debug=False)
