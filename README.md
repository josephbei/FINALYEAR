# School Permission Management System (starter)

This repository contains a minimal Django starter app implementing a Permission System for a school.

Features included:
- Parent and Student models. Students inherit contact info from assigned Parent.
- Parent registration (creates a User + Parent profile) and Student registration (no student login).
- PermissionRequest model with normal and emergency types.
- Views for teachers/discipline/headmaster to approve/reject/escalate requests.
- PDF exit-pass generation hook (WeasyPrint recommended) and notification hooks for email + Twilio SMS.

Setup (local):
1. Install Python 3.10+ and create a virtualenv
   python -m venv .venv
   source .venv/bin/activate
2. pip install -r requirements.txt
3. Create a .env file or set environment variables for SECRET_KEY, DJANGO_DEBUG, TWILIO*, SITE_URL if desired.
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver

Default development email backend is console. Configure SMTP and Twilio in settings for real notifications.

Branch: permission-system-starter
