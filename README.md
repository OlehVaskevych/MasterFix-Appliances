# Appliance Repair Landing Page

Landing page for a home appliance repair company in the USA.

## Tech Stack

- **Backend:** Python 3.12, Django 5.x
- **Database:** PostgreSQL 16
- **Containerization:** Docker & Docker Compose

## Features

- [x] Header with navigation
- [x] Services section (4+ services)
- [x] Booking form with validation (name, phone, problem description)
- [x] Footer with contact information
- [x] Responsive design
- [x] Form data persistence to database

## Project Structure

```
├── backend/                    # Django application
│   ├── config/                 # Project configuration
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Base settings
│   │   │   ├── development.py # Dev settings
│   │   │   └── production.py  # Prod settings
│   │   ├── __init__.py
│   │   ├── urls.py            # Root URL configuration
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── core/              # Core app (landing page, static pages)
│   │   │   ├── __init__.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── apps.py 
│   │   ├── bookings/          # Bookings app (form handling)
│   │   │   ├── migrations/
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── forms.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   └── services/
│   │       ├── migrations/
│   │       ├── __init__.py
│   │       ├── admin.py
│   │       ├── apps.py
│   │       ├── models.py
│   │       ├── urls.py
│   │       └── views.py
│   ├── templates/             # Global templates
│   │   ├── landing.html
│   │   └── base.html
│   ├── static/                # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── __init__.py
│   ├── manage.py
│   └── requirements.txt       # All dependencies
├── docker/
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── Dockerfile.prod
│   └── nginx/
│       ├── Dockerfile
│       └── nginx.conf
├── docker-compose.yml          # Development environment
├── docker-compose.prod.yml     # Production environment
├── .env.example                # Environment variables template
├── .gitignore
└── README.md
```

## Docker Services

| Service    | Port  | Description                          |
|------------|-------|--------------------------------------|
| backend    | 8000  | Django application (Gunicorn)        |
| db         | 5432  | PostgreSQL database                  |
| nginx      | 80    | Nginx reverse proxy (production)     |

## Prerequisites

- Docker >= 24.0
- Docker Compose >= 2.20
- Git

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd appliance-repair-landing
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Build and run with Docker

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d
```

### 4. Run migrations

```bash
docker-compose exec backend python manage.py migrate
```

### 5. Create superuser (optional)

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Access the application

- Landing Page: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## Development

### Running without Docker

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Running tests

```bash
docker-compose exec backend pytest
```

### Code formatting

```bash
# Black for Python
docker-compose exec backend black .

# Flake8 for linting
docker-compose exec backend flake8
```

## Work Plan

### Phase 1: Project Setup
- [x] Initial project structure
- [x] README.md documentation
- [x] Docker configuration
- [x] Environment variables setup

### Phase 2: Backend Development
- [x] Django project initialization
- [x] Database models (Booking)
- [x] Views and URL routing
- [x] Form validation (server-side)
- [ ] Admin panel configuration

### Phase 3: Frontend Development
- [x] Base HTML template
- [x] Header component with navigation
- [x] Services section (4 services)
- [x] Booking form with validation
- [x] Footer component
- [x] Responsive CSS styles

### Phase 4: Integration & Testing
- [x] API endpoint for form submission
- [ ] Unit tests
- [ ] Integration tests

### Phase 5: Deployment Preparation
- [ ] Production Docker configuration
- [ ] Nginx configuration
- [ ] Static files collection
- [ ] Security hardening

## API Endpoints

| Method | Endpoint           | Description              |
|--------|-------------------|--------------------------|
| GET    | /                 | Landing page             |
| POST   | /api/bookings/    | Submit booking form      |
| GET    | /admin/           | Django admin panel       |

## Environment Variables

See `.env.example` for all available environment variables.

## License

MIT License

## Contact

For questions or support, please contact the development team.
