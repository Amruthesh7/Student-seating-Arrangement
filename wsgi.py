#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

from app import app, db

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

# This is the WSGI application object
application = app

if __name__ == "__main__":
    app.run()
