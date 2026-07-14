# database.py -  Responsible for Database Operations
from flask_sqlalchemy import SQLAlchemy
from models import db, Student

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")
        
        if Student.query.count() == 0:
            add_sample_data()

def add_sample_data():
    sample_students = [
        Student(
            student_name='Tukahebwa Ritah',
            registration_number='24/U/1100/PS',
            email=' ritah@mak.ac.ug',
            programme='BSSE'
        ),
        Student(
            student_name='Owen Micheal',
            registration_number='24/U/1101/EVE',
            email='owen.micheal@mak.ac.ug',
            programme='Information Technology'
        )
    ]
    
    for student in sample_students:
        db.session.add(student)
    db.session.commit()
    print("📚 Sample data added!")

def get_all_students():
    return Student.query.filter_by(is_active=True).all()

def get_student_by_name(name):
    return Student.query.filter(
        Student.student_name.contains(name),
        Student.is_active == True
    ).all()

def get_student_by_registration(registration_number):
    return Student.query.filter_by(registration_number=registration_number).first()

def add_student(student_data):
    try:
        existing = get_student_by_registration(student_data['registration_number'])
        if existing:
            return False, "Registration number already exists!", None
        
        existing_email = Student.query.filter_by(email=student_data['email']).first()
        if existing_email:
            return False, "Email already registered!", None
        
        new_student = Student(
            student_name=student_data['student_name'],
            registration_number=student_data['registration_number'],
            email=student_data['email'],
            programme=student_data['programme']
        )
        
        db.session.add(new_student)
        db.session.commit()
        return True, "Student registered successfully!", new_student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None

def add_student(student_data):
    try:
        existing = get_student_by_registration(student_data['registration_number'])
        if existing:
            return False, "Registration number already exists!", None

        existing_email = Student.query.filter_by(email=student_data['email']).first()
        if existing_email:
            return False, "Email already registered!", None

        new_student = Student(
            student_name=student_data['student_name'],
            registration_number=student_data['registration_number'],
            email=student_data['email'],
            programme=student_data['programme']
        )

        db.session.add(new_student)
        db.session.commit()
        return True, "Student registered successfully!", new_student

    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None
def get_student_by_id(student_id):
    return Student.query.get(student_id)


def update_student(student_id, student_data):

    student = Student.query.get(student_id)

    if student:

        student.student_name = student_data['student_name']
        student.registration_number = student_data['registration_number']
        student.email = student_data['email']
        student.programme = student_data['programme']

        db.session.commit()

        return True, "Student updated successfully!"

    return False, "Student not found."


def delete_student(student_id):

    student = Student.query.get(student_id)

    if student:

        db.session.delete(student)

        db.session.commit()

        return True, "Student deleted successfully."

    return False, "Student not found."