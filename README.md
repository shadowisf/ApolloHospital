# APOLLO HOSPITAL
![ImageApolloHospital1](https://github.com/shadowisf/ApolloHospital/assets/97739695/dc955834-1f30-47e6-bd72-a169a6c173f9)

&emsp;

## DEPENDENCIES
1. XAMPP
2. Python
3. Python libraries mentioned in `requirements.txt`

&emsp;

## SETUP
1. Clone and open this repository in VSCODE
2. Install Python libraries by entering `pip install -r requirements.txt` in VSCODE terminal
1. Install XAMPP and turn on SQL Server
2. Go to localhost in web browser > phpMyAdmin > SQL console tab
3. Paste the SQL query provided in the repository or at the last section of this README
4. Run `main.py`
5. Register and login. Note that doctor records will be populated from the get-go

&emsp;

## SQL
```
CREATE DATABASE apollo_hms;

USE apollo_hms;

CREATE TABLE receptionist_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_username (username),
    UNIQUE KEY unique_email (email)
);

CREATE TABLE doctor_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_username (username),
    UNIQUE KEY unique_email (email)
);

CREATE TABLE staff_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_username (username),
    UNIQUE KEY unique_email (email)
);

CREATE TABLE patient (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fullname VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(fullname) > 0),
    phone VARCHAR(15) NOT NULL CHECK (CHAR_LENGTH(phone) > 0),
    dob DATE,
    address VARCHAR(255),
    gender ENUM('Male', 'Female', 'Other'),
    email VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(email) > 0),
    
    UNIQUE (fullname),
    UNIQUE (phone),
    UNIQUE (email)
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    specialty VARCHAR(100) NOT NULL,
    availability JSON,
    availability_start_time TIME NOT NULL,
    availability_end_time TIME NOT NULL			
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_day DATE,
    appointment_time TIME,
    room_number VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    doctor_name VARCHAR(255) NOT NULL,
    symptoms TEXT NOT NULL,
    prescription TEXT NOT NULL,
    medical_test VARCHAR(255),
    record_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO doctors (name, email, room_number, specialty, availability, availability_start_time, availability_end_time)
VALUES
    ('Dr. Johnson', 'drjohnson@gmail.com', 'Room 102', 'Cardiology', '["Tuesday", "Thursday", "Saturday"]', '09:00:00', '17:00:00'),
    ('Dr. Brown', 'drbrown@gmail.com', 'Room 201', 'Dermatology', '["Monday", "Tuesday", "Wednesday"]', '08:30:00', '15:30:00'),
    ('Dr. Miller', 'drmiller@gmail.com', 'Room 202', 'Dermatology', '["Wednesday", "Thursday", "Friday"]', '09:30:00', '16:30:00'),
    ('Dr. Wilson', 'drwilson@gmail.com', 'Room 301', 'Orthopedics', '["Sunday", "Tuesday", "Thursday"]', '08:15:00', '17:15:00'),
    ('Dr. Anderson', 'dranderson@gmail.com', 'Room 302', 'Orthopedics', '["Monday", "Wednesday", "Friday"]', '09:15:00', '18:15:00'),
    ('Dr. Thomas', 'drthomas@gmail.com', 'Room 401', 'Oncology', '["Tuesday", "Thursday", "Saturday"]', '08:00:00', '16:00:00'),
    ('Dr. Jackson', 'drjackson@gmail.com', 'Room 402', 'Oncology', '["Sunday", "Monday", "Wednesday"]', '09:00:00', '17:00:00'),
    ('Dr. Harris', 'drharris@gmail.com', 'Room 501', 'Neurology', '["Sunday", "Monday", "Friday"]', '08:30:00', '15:30:00'),
    ('Dr. Adams', 'dradams@gmail.com', 'Room 502', 'Neurology', '["Tuesday", "Wednesday", "Saturday"]', '09:30:00', '16:30:00');

INSERT INTO doctors (name, email, room_number, specialty, availability, availability_start_time, availability_end_time)
VALUES
    ('Dr. White', 'dr.white@gmail.com', 'Room 601', 'Pediatrics', '["Monday", "Wednesday", "Friday"]', '08:00:00', '16:00:00'),
    ('Dr. Hall', 'dr.hall@gmail.com', 'Room 602', 'Pediatrics', '["Tuesday", "Thursday", "Saturday"]', '09:00:00', '17:00:00'),
    ('Dr. Young', 'dr.young@gmail.com', 'Room 701', 'Gynecology', '["Monday", "Thursday", "Saturday"]', '08:30:00', '15:30:00'),
    ('Dr. Green', 'dr.green@gmail.com', 'Room 702', 'Gynecology', '["Tuesday", "Wednesday", "Friday"]', '09:00:00', '16:00:00'),
    ('Dr. Hill', 'dr.hill@gmail.com', 'Room 801', 'Urology', '["Sunday", "Tuesday", "Thursday"]', '08:15:00', '17:15:00'),
    ('Dr. Turner', 'dr.turner@gmail.com', 'Room 802', 'Urology', '["Monday", "Wednesday", "Friday"]', '09:15:00', '18:15:00'),
    ('Dr. Walker', 'dr.walker@gmail.com', 'Room 901', 'Ophthalmology', '["Tuesday", "Thursday", "Saturday"]', '08:00:00', '16:00:00'),
    ('Dr. Brooks', 'dr.brooks@gmail.com', 'Room 902', 'Ophthalmology', '["Sunday", "Monday", "Wednesday"]', '09:00:00', '17:00:00'),
    ('Dr. King', 'dr.king@gmail.com', 'Room 1001', 'Dentistry', '["Sunday", "Tuesday", "Thursday"]', '08:30:00', '15:30:00'),
    ('Dr. Ross', 'dr.ross@gmail.com', 'Room 1002', 'Dentistry', '["Tuesday", "Wednesday", "Saturday"]', '09:30:00', '16:30:00');

INSERT INTO doctors (name, email, room_number, specialty, availability, availability_start_time, availability_end_time)
VALUES
    ('Dr. Smith', 'dr.smith@gmail.com', 'Room 1101', 'General Practitioner', '["Monday", "Wednesday", "Friday"]', '08:00:00', '16:00:00'),
    ('Dr. Turner1', 'dr.turner1@gmail.com', 'Room 1102', 'General Practitioner', '["Tuesday", "Thursday", "Saturday"]', '09:00:00', '17:00:00'),
    ('Dr. Davis', 'dr.davis@gmail.com', 'Room 1201', 'General Practitioner', '["Monday", "Thursday", "Saturday"]', '08:30:00', '15:30:00'),
    ('Dr. Robinson', 'dr.robinson@gmail.com', 'Room 1202', 'General Practitioner', '["Tuesday", "Wednesday", "Friday"]', '09:00:00', '16:00:00'),
    ('Dr. Wilson1', 'dr.wilson1@gmail.com', 'Room 1301', 'General Practitioner', '["Sunday", "Tuesday", "Thursday"]', '08:15:00', '17:15:00');
```
