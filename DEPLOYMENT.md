# Vercel + Railway integration notes

This branch sets up a small Django REST backend and a Next.js frontend (inside /frontend).

Deployment plan (recommended):
1. Deploy Django backend to Railway (or Render) and set environment variables.
   - Set the build command: pip install -r requirements.txt && python manage.py migrate
   - Start command: gunicorn permission_system.wsgi --bind 0.0.0.0:$PORT
   - Set env vars: SECRET_KEY, DJANGO_DEBUG=0, SITE_URL=https://<railway-url>, TWILIO_*, EMAIL settings, CORS_ALLOW_ALL_ORIGINS=0, CORS_ALLOWED_ORIGINS=https://<your-vercel-domain>
2. Deploy frontend to Vercel
   - In Vercel, create a new project from this repo. Set the "Root Directory" for the project to "/frontend" when prompted.
   - Set environment variable NEXT_PUBLIC_API_URL to your Railway backend URL + '/api'
   - Vercel will detect Next.js and build automatically.

Local testing:
- Run Django locally: python manage.py migrate; python manage.py runserver
- Run frontend: cd frontend; npm install; npm run dev
- Make sure NEXT_PUBLIC_API_URL points to http://localhost:8000/api when testing locally.
