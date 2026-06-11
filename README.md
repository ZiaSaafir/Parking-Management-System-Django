Parking Management System

A professional Django-based Parking Management System for managing vehicle entry, parking slots, tickets, payments, receipts, reports, dashboard analytics, and role-based access control.

Live Demo:

https://parking-management-system-2s1w.onrender.com

Features
User authentication
Role-based access control
Admin
Manager
Operator
Vehicle entry and exit management
Owner name and phone record
Automatic and manual parking slot allocation
Vehicle-type based slot suggestion
Parking ticket generation
Payment processing
Printable receipt
Active vehicle tracking
Vehicle history
Daily, monthly, yearly, and custom reports
CSV/Excel export
Parking slot management
Add slot
Edit slot
Delete slot
Maintenance status
Slot type support
Dashboard with charts and analytics
Deployed online on Render
Tech Stack
Backend: Django
Frontend: HTML, CSS, JavaScript
Database:
Local: MySQL
Deployment: PostgreSQL
Charts: Chart.js
Deployment: Render
Authentication: Django Auth
User Roles
Admin
Full system access
Manage parking slots
Manage operations
View dashboard
View reports
Manager
View reports
View vehicle history
Monitor system activity
Operator
Vehicle entry
Vehicle exit
Active vehicles
Receipt generation
Software Design Principles Used
Layered architecture
Service layer design
Separation of concerns
Modular Django apps
Role-based access control
Environment-based configuration
Reusable templates
Clean project structure
Project Structure
parking/
├── accounts/
├── config/
├── parking/
├── payments/
├── reports/
├── services/
├── static/
│   └── css/
├── templates/
│   ├── accounts/
│   ├── dashboard/
│   ├── includes/
│   ├── layouts/
│   ├── operations/
│   ├── payments/
│   ├── reports/
│   └── slots/
├── build.sh
├── requirements.txt
└── manage.py
Local Installation

Clone the repository:

git clone https://github.com/ZiaSaafir/Parking-Management-System-Django.git
cd Parking-Management-System-Django

Create virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create .env file:

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=parking_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

DATABASE_URL=

Run migrations:

python manage.py migrate

Create superuser:

python manage.py createsuperuser

Run server:

python manage.py runserver

Open:

http://127.0.0.1:8000/
Default Workflow
Admin creates parking slots.
Operator enters vehicle details.
System suggests a compatible parking slot.
Operator confirms or manually changes the slot.
Ticket is generated.
On vehicle exit, payment is processed.
Receipt is generated.
Admin/Manager views reports and dashboard analytics.
Deployment

This project is deployed on Render using:

Gunicorn
WhiteNoise
PostgreSQL
Environment variables
Render build script
Future Improvements
PDF receipt download
Full user management panel
Activity logs
Parking map visualization
REST API
Mobile app support
Docker deployment
Backup and restore system
Author

Developed by Zia Ullah
FAST NUCES Peshawar
GitHub: ZiaSaafir