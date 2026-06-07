Smart Parking Management System

A scalable and maintainable Parking Management System built with Django, MySQL, HTML, CSS, and JavaScript. This project is being developed following software engineering principles, layered architecture, service-based design, and clean coding practices.

Project Overview

The Smart Parking Management System is designed to automate parking operations such as vehicle entry, parking slot allocation, ticket generation, payment processing, and reporting.

The goal is to build a real-world enterprise-level parking solution rather than a simple academic project.

Features
Current Features
Vehicle Registration
Vehicle Type Management
Vehicle Validation
Service Layer Architecture
Professional Django Project Structure
Flash Messages and Validation Handling
Upcoming Features
Automatic Parking Slot Allocation
Parking Ticket Generation
Vehicle Exit Management
Parking Fee Calculation
Payment Processing
Customer Management
Parking History Tracking
Dashboard Analytics
Reporting System
QR Code Ticket Support
Monthly Membership Plans
Technology Stack
Backend
Python
Django
MySQL
Frontend
HTML5
CSS3
JavaScript
Development Tools
Git
GitHub
VS Code
Ubuntu Linux
Project Structure
accounts/
config/
parking/
payments/
reports/
services/
static/
templates/
manage.py
Service Layer
services/
├── parking_service.py
├── slot_service.py
└── payment_service.py

The service layer contains business logic and keeps views clean and maintainable.

Software Engineering Principles

This project follows:

Separation of Concerns (SoC)
Single Responsibility Principle (SRP)
Layered Architecture
Modular Design
Reusable Services
Maintainable Code Structure
Scalability-Oriented Development
Database Design

Main Entities:

VehicleType
Vehicle
ParkingSlot
ParkingTicket
Payment

Future Entities:

Customer
MembershipPlan
ParkingHistory
Notification
Future Roadmap
Phase 1
Vehicle Entry
Slot Allocation
Ticket Generation
Phase 2
Vehicle Exit
Payment Module
Fee Calculation
Phase 3
Reports
Analytics Dashboard
Customer Management
Phase 4
REST API
Mobile Integration
QR Code Support
Online Deployment
Installation
git clone https://github.com/ZiaSaafir/Parking-Management-System-Django.git

cd Parking-Management-System-Django

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
Author

Ziaullah

BS Computer Science

FAST University Peshawar

Focused on Full-Stack Development, Software Engineering, and Artificial Intelligence.

Project Status

Currently under active development.
New features and improvements are being added incrementally following professional software development practices.