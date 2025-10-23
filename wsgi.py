#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

from app import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
