# Student Seating Arrangement Portal

A comprehensive web application built with Python Flask for managing student seating arrangements during exams. The system ensures that students with the same subject code are not seated on the same bench, maintaining exam integrity.

## Features

- **Student Management**: Add, view, and manage student information including subject codes
- **Room Management**: Configure exam rooms with capacity and bench information
- **Smart Seating Algorithm**: Automatically generates seating arrangements ensuring:
  - Students with same subject code are placed on different benches
  - Maximum 2 students per bench
  - Fair distribution across available rooms
  - Optimal room capacity utilization
- **Modern Web Interface**: Responsive design with Bootstrap 5
- **Real-time Dashboard**: Overview of students, rooms, and arrangements

## Installation & Running Instructions

### **Prerequisites**
- Python 3.7 or higher installed on your system
- pip (Python package installer)

### **Step-by-Step Instructions:**

#### **1. Navigate to the Project Directory**
```bash
cd C:\Users\Amrut\OneDrive\Desktop\student-seating-arrangement
```

#### **2. Install Required Dependencies**
```bash
pip install -r requirements.txt
```
This will install:
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-WTF 1.1.1
- WTForms 3.0.1
- Werkzeug 2.3.7

#### **3. Create Sample Data (Optional but Recommended)**
```bash
python sample_data.py
```
This creates:
- 21 sample students across 5 different subject codes
- 5 sample rooms with varying capacities
- Ready-to-test data for immediate use

#### **4. Start the Flask Application**
```bash
python app.py
```

#### **5. Access the Application**
Open your web browser and go to:
```
http://localhost:5000
```

### **Quick Test:**

1. Go to **"Generate"** → **"Generate Seating Arrangement"**
2. Select today's date
3. Click **"Generate Seating Arrangement"**
4. Go to **"Arrangements"** to see the results

You'll notice that students with the same subject code (like CS101) are placed on different benches, ensuring exam integrity!

### **Troubleshooting:**

**If you get "Module not found" errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If the database seems corrupted:**
```bash
# Delete the database file and recreate
del seating_arrangement.db
python sample_data.py
```

**If port 5000 is busy:**
The app will automatically find an available port and display it in the terminal.

### **Stopping the Application:**
Press `Ctrl + C` in the terminal where the Flask app is running.

## Usage

### 1. Add Students
- Navigate to "Students" → "Add Student"
- Fill in student ID, name, subject code, and email
- Subject codes are crucial for the seating algorithm

### 2. Add Rooms
- Navigate to "Rooms" → "Add Room"
- Specify room number, total capacity, and number of benches
- The system assumes 2 students per bench

### 3. Generate Seating Arrangement
- Navigate to "Generate" → "Generate Seating Arrangement"
- Select the exam date
- Click "Generate Seating Arrangement"
- The system will automatically assign students to rooms and benches

### 4. View Arrangements
- Navigate to "Arrangements" to see all seating assignments
- View detailed information including room, bench, and seat numbers

## Algorithm Details

The seating arrangement algorithm works as follows:

1. **Grouping**: Students are grouped by their subject codes
2. **Room Assignment**: For each student, the system tries to find an available bench
3. **Subject Separation**: Students with the same subject code cannot be placed on the same bench
4. **Capacity Management**: Maximum 2 students per bench
5. **Fair Distribution**: Students are distributed evenly across available rooms

## Database Schema

- **Students**: Student information including ID, name, subject code, and email
- **Rooms**: Room details including number, capacity, and bench count
- **SeatingArrangements**: Assignment records linking students to specific rooms, benches, and seats

## File Structure

```
student-seating-arrangement/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sample_data.py        # Sample data generator
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── add_student.html
│   ├── rooms.html
│   ├── add_room.html
│   ├── arrangements.html
│   └── generate_arrangement.html
└── static/
    └── style.css        # Custom CSS styles
```

## Sample Data

The `sample_data.py` script creates:
- 21 students across 5 different subject codes
- 5 rooms with varying capacities
- Ready-to-test data for immediate use

## Customization

### Adding New Subject Codes
Simply add students with new subject codes through the web interface. The algorithm will automatically handle them.

### Modifying Room Capacity
Update room information through the "Rooms" section. The system will recalculate seating arrangements accordingly.

### Styling
Modify `static/style.css` to customize the appearance of the application.

## Troubleshooting

### Common Issues

1. **"No students or rooms available"**
   - Ensure you have added both students and rooms before generating arrangements

2. **"Students could not be assigned"**
   - Check if you have sufficient room capacity
   - Verify that the number of benches can accommodate all students

3. **Database errors**
   - Delete the `seating_arrangement.db` file and restart the application
   - Run `sample_data.py` again to recreate the database

## Technical Requirements

- Python 3.7+
- Flask 2.3.3
- SQLAlchemy 3.0.5
- Modern web browser with JavaScript enabled

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

---

**Note**: This system is designed for educational purposes and can be adapted for various seating arrangement needs in schools, colleges, and examination centers.

