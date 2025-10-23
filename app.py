from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
import random
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
# Handle database URL for different environments
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Production environment (Railway, Render, Heroku)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Development environment
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seating_arrangement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    subject_code = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.name} ({self.student_id})>'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    benches = db.Column(db.Integer, nullable=False)  # Number of benches in the room
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Room {self.room_number}>'

class SeatingArrangement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    bench_number = db.Column(db.Integer, nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('seating_arrangements', lazy=True))
    room = db.relationship('Room', backref=db.backref('seating_arrangements', lazy=True))

    def __repr__(self):
        return f'<SeatingArrangement Student: {self.student_id}, Room: {self.room_id}, Bench: {self.bench_number}>'

# Forms
class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=1, max=20)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=100)])
    subject_code = StringField('Subject Code', validators=[DataRequired(), Length(min=1, max=10)])
    email = StringField('Email', validators=[DataRequired(), Length(min=1, max=120)])
    submit = SubmitField('Add Student')

class RoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[DataRequired(), Length(min=1, max=20)])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    benches = IntegerField('Number of Benches', validators=[DataRequired()])
    submit = SubmitField('Add Room')

class ExamForm(FlaskForm):
    exam_date = StringField('Exam Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Generate Seating Arrangement')

# Seating Algorithm
def generate_seating_arrangement(exam_date):
    """
    Generate seating arrangement ensuring students with same subject code
    don't sit on the same bench
    """
    # Clear existing arrangements for this date
    SeatingArrangement.query.filter_by(exam_date=exam_date).delete()
    
    # Get all students and rooms
    students = Student.query.all()
    rooms = Room.query.all()
    
    if not students or not rooms:
        return False, "No students or rooms available"
    
    # Group students by subject code
    subject_groups = {}
    for student in students:
        if student.subject_code not in subject_groups:
            subject_groups[student.subject_code] = []
        subject_groups[student.subject_code].append(student)
    
    # Create a list to track bench assignments
    bench_assignments = {}  # {room_id: {bench_number: [subject_codes]}}
    
    # Initialize bench assignments for each room
    for room in rooms:
        bench_assignments[room.id] = {}
        for bench in range(1, room.benches + 1):
            bench_assignments[room.id][bench] = []
    
    arrangements = []
    unassigned_students = []
    
    # Try to assign students
    for subject_code, student_list in subject_groups.items():
        for student in student_list:
            assigned = False
            
            # Try each room
            for room in rooms:
                if assigned:
                    break
                    
                # Try each bench in the room
                for bench_num in range(1, room.benches + 1):
                    if assigned:
                        break
                    
                    # Check if this bench already has a student with the same subject code
                    if subject_code in bench_assignments[room.id][bench_num]:
                        continue
                    
                    # Check if bench has capacity (assuming 2 students per bench)
                    current_bench_occupancy = len(bench_assignments[room.id][bench_num])
                    if current_bench_occupancy >= 2:
                        continue
                    
                    # Assign student to this bench
                    seat_num = current_bench_occupancy + 1
                    arrangement = SeatingArrangement(
                        student_id=student.id,
                        room_id=room.id,
                        bench_number=bench_num,
                        seat_number=seat_num,
                        exam_date=exam_date
                    )
                    arrangements.append(arrangement)
                    bench_assignments[room.id][bench_num].append(subject_code)
                    assigned = True
            
            if not assigned:
                unassigned_students.append(student)
    
    # Save arrangements to database
    try:
        for arrangement in arrangements:
            db.session.add(arrangement)
        db.session.commit()
        return True, f"Successfully assigned {len(arrangements)} students. {len(unassigned_students)} students could not be assigned."
    except Exception as e:
        db.session.rollback()
        return False, f"Error saving arrangements: {str(e)}"

# Routes
@app.route('/health')
def health_check():
    """Health check endpoint for deployment verification"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'message': 'Student Seating Arrangement Portal is running',
        'database': db_status
    })

@app.route('/')
def index():
    total_students = Student.query.count()
    total_rooms = Room.query.count()
    total_arrangements = SeatingArrangement.query.count()
    
    return render_template('index.html', 
                         total_students=total_students,
                         total_rooms=total_rooms,
                         total_arrangements=total_arrangements)

@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            student_id=form.student_id.data,
            name=form.name.data,
            subject_code=form.subject_code.data,
            email=form.email.data
        )
        try:
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            flash(f'Error adding student: {str(e)}', 'error')
    
    return render_template('add_student.html', form=form)

@app.route('/rooms')
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(
            room_number=form.room_number.data,
            capacity=form.capacity.data,
            benches=form.benches.data
        )
        try:
            db.session.add(room)
            db.session.commit()
            flash('Room added successfully!', 'success')
            return redirect(url_for('rooms'))
        except Exception as e:
            flash(f'Error adding room: {str(e)}', 'error')
    
    return render_template('add_room.html', form=form)

@app.route('/arrangements')
def arrangements():
    arrangements = SeatingArrangement.query.join(Student).join(Room).all()
    return render_template('arrangements.html', arrangements=arrangements)

@app.route('/generate_arrangement', methods=['GET', 'POST'])
def generate_arrangement():
    form = ExamForm()
    if form.validate_on_submit():
        exam_date = datetime.strptime(form.exam_date.data, '%Y-%m-%d').date()
        success, message = generate_seating_arrangement(exam_date)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('arrangements'))
    
    return render_template('generate_arrangement.html', form=form)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students'))

@app.route('/delete_room/<int:room_id>')
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    try:
        db.session.delete(room)
        db.session.commit()
        flash('Room deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting room: {str(e)}', 'error')
    
    return redirect(url_for('rooms'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Get port from environment variable or use 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
