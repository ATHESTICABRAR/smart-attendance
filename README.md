📌 Smart Attendance System
(Location-Based + Barcode Attendance Website)

🧠 Project Overview
This project is a Smart Attendance Website where students can mark attendance by scanning the barcode on their ID card.
Attendance is allowed only when the student is physically inside the college, verified using live GPS location.

The system stores attendance data in a central server database and provides a secure dashboard for lecturers to view, edit, lock, and share attendance reports.

🎯 Problem Statement
Traditional attendance systems:

Allow proxy attendance

Require biometric hardware

Are time-consuming

Lack centralized control

✅ Solution
This system:

Prevents proxy attendance using GPS verification

Uses ID card barcode (no biometric device needed)

Stores data securely on the server

Gives full control to lecturers

Allows quick WhatsApp sharing of attendance

⚙️ Features
👨‍🎓 Student
Scan barcode from ID card

Attendance allowed only inside college

Can mark only their own attendance

Cannot view or edit records

👨‍🏫 Lecturer
Secure login

View all attendance records

Edit attendance (Present / Absent)

Lock attendance

Share attendance report via WhatsApp

📍 Location-Based Attendance
Uses HTML5 Geolocation API

Compares student’s live GPS location with college location

Attendance allowed only within 150 meters radius

🪪 Barcode Attendance
Barcode value = Student ID

Barcode scanner works like a keyboard

No additional hardware coding required

🗄️ Data Storage
Stored in SQLite database

Centralized storage (not browser-based)

Secure and permanent records

🧱 Technology Stack
Layer	Technology
Frontend	HTML, CSS, JavaScript
Backend	Flask (Python 3.7)
Database	SQLite
Location	HTML5 Geolocation
Authentication	Session-based login
Version Control	GitHub
