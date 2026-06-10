# Parking Management System

A professional Django-based Parking Management System built for managing vehicle entry, parking slots, tickets, payments, receipts, reports, and role-based access control.

## Features

- User authentication
- Role-based access control
  - Admin
  - Manager
  - Operator
- Vehicle entry and exit management
- Owner name and phone record
- Automatic and manual parking slot allocation
- Vehicle-type based slot suggestion
- Parking ticket generation
- Payment processing
- Printable receipt
- Active vehicle tracking
- Vehicle history
- Daily / monthly / yearly / custom reports
- CSV/Excel export
- Parking slot management
  - Add slot
  - Edit slot
  - Delete slot
  - Maintenance status
- Dashboard with charts and analytics

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Django
- Database: MySQL
- Charts: Chart.js
- Authentication: Django Auth

## User Roles

### Admin
- Full system access
- Manage slots
- View reports
- Manage operations

### Manager
- View reports
- View vehicle history
- Monitor system activity

### Operator
- Vehicle entry
- Vehicle exit
- Active vehicles
- Receipt generation

## Project Structure

```text
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
└── manage.py

Installation

Clone the repository:

git clone https://github.com/ZiaSaafir/Parking-Management-System-Django.git
cd Parking-Management-System-Django

Create virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py makemigrations
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
System suggests compatible parking slot.
Operator confirms or changes slot.
Ticket is generated.
On exit, payment is processed.
Receipt is generated.
Manager/Admin views reports.
Future Improvements
PDF receipt download
Full user management panel
Activity logs
Parking map visualization
REST API
Mobile app support
Docker deployment
Cloud deployment
Author

Developed by Zia Ullah
FAST NUCES Peshawar
GitHub: ZiaSaafir


Then run:

```bash
pip freeze > requirements.txt
git add .
git commit -m "Update README and prepare project for deployment"
git push