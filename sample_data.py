#!/usr/bin/env python3
"""
Sample data generator for Student Seating Arrangement Portal
Run this script to populate the database with sample data for testing
"""

from app import app, db, Student, Room
from datetime import datetime

def create_sample_data():
    """Create sample students and rooms for testing"""
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Sample students with different subject codes
        sample_students = [
            # Computer Science students
            {"student_id": "CS001", "name": "Alice Johnson", "subject_code": "CS101", "email": "alice.johnson@email.com"},
            {"student_id": "CS002", "name": "Bob Smith", "subject_code": "CS101", "email": "bob.smith@email.com"},
            {"student_id": "CS003", "name": "Charlie Brown", "subject_code": "CS101", "email": "charlie.brown@email.com"},
            {"student_id": "CS004", "name": "Diana Prince", "subject_code": "CS101", "email": "diana.prince@email.com"},
            {"student_id": "CS005", "name": "Eve Wilson", "subject_code": "CS101", "email": "eve.wilson@email.com"},
            
            # Mathematics students
            {"student_id": "MATH001", "name": "Frank Miller", "subject_code": "MATH201", "email": "frank.miller@email.com"},
            {"student_id": "MATH002", "name": "Grace Lee", "subject_code": "MATH201", "email": "grace.lee@email.com"},
            {"student_id": "MATH003", "name": "Henry Davis", "subject_code": "MATH201", "email": "henry.davis@email.com"},
            {"student_id": "MATH004", "name": "Ivy Chen", "subject_code": "MATH201", "email": "ivy.chen@email.com"},
            
            # Physics students
            {"student_id": "PHY001", "name": "Jack Wilson", "subject_code": "PHY301", "email": "jack.wilson@email.com"},
            {"student_id": "PHY002", "name": "Kate Anderson", "subject_code": "PHY301", "email": "kate.anderson@email.com"},
            {"student_id": "PHY003", "name": "Liam Taylor", "subject_code": "PHY301", "email": "liam.taylor@email.com"},
            {"student_id": "PHY004", "name": "Maya Patel", "subject_code": "PHY301", "email": "maya.patel@email.com"},
            {"student_id": "PHY005", "name": "Noah Garcia", "subject_code": "PHY301", "email": "noah.garcia@email.com"},
            
            # Chemistry students
            {"student_id": "CHEM001", "name": "Olivia Martinez", "subject_code": "CHEM401", "email": "olivia.martinez@email.com"},
            {"student_id": "CHEM002", "name": "Peter Rodriguez", "subject_code": "CHEM401", "email": "peter.rodriguez@email.com"},
            {"student_id": "CHEM003", "name": "Quinn Thompson", "subject_code": "CHEM401", "email": "quinn.thompson@email.com"},
            
            # Biology students
            {"student_id": "BIO001", "name": "Rachel White", "subject_code": "BIO501", "email": "rachel.white@email.com"},
            {"student_id": "BIO002", "name": "Samuel Harris", "subject_code": "BIO501", "email": "samuel.harris@email.com"},
            {"student_id": "BIO003", "name": "Tina Clark", "subject_code": "BIO501", "email": "tina.clark@email.com"},
            {"student_id": "BIO004", "name": "Uma Lewis", "subject_code": "BIO501", "email": "uma.lewis@email.com"},
        ]
        
        # Sample rooms
        sample_rooms = [
            {"room_number": "A101", "capacity": 20, "benches": 10},
            {"room_number": "A102", "capacity": 16, "benches": 8},
            {"room_number": "B201", "capacity": 24, "benches": 12},
            {"room_number": "B202", "capacity": 18, "benches": 9},
            {"room_number": "C301", "capacity": 22, "benches": 11},
        ]
        
        print("Creating sample students...")
        for student_data in sample_students:
            student = Student(**student_data)
            db.session.add(student)
        
        print("Creating sample rooms...")
        for room_data in sample_rooms:
            room = Room(**room_data)
            db.session.add(room)
        
        try:
            db.session.commit()
            print(f"Successfully created {len(sample_students)} students and {len(sample_rooms)} rooms!")
            print("\nSample data includes:")
            print("- 5 Computer Science students (CS101)")
            print("- 4 Mathematics students (MATH201)")
            print("- 5 Physics students (PHY301)")
            print("- 3 Chemistry students (CHEM401)")
            print("- 4 Biology students (BIO501)")
            print("- 5 rooms with varying capacities")
            print("\nYou can now run the Flask app and test the seating arrangement system!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating sample data: {str(e)}")

if __name__ == "__main__":
    create_sample_data()
