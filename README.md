# 📚 Book Catalog API

A comprehensive RESTful API for managing a book catalog system built with Django REST Framework.

## ✨ Features

- **📖 Book Management**: Full CRUD operations for book inventory
- **📋 Borrowing System**: Checkout and return books with due date tracking
- **⭐ Rating System**: Rate and review books (1-5 stars)
- **🔐 JWT Authentication**: Secure token-based authentication
- **👥 Role-Based Access**: Administrators and Members with different permissions
- **📄 API Documentation**: Interactive Swagger UI and ReDoc

## 🛡️ Security Features

This application implements industry-standard security measures:

| Protection | Implementation |
|------------|----------------|
| **SQL Injection** | Django ORM with parameterized queries |
| **XSS (Cross-Site Scripting)** | Content-Type sniffing prevention, XSS filter headers |
| **CSRF** | Django CSRF middleware with secure cookies |
| **Clickjacking** | X-Frame-Options: DENY |
| **HTTPS** | SSL redirect enforced in production |
| **HSTS** | Strict Transport Security enabled |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd book-catalog-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create user groups
python manage.py setup_groups

# Seed sample books (optional)
python manage.py seed_books

# Start development server
python manage.py runserver
```

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Get JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Get current user profile |

### Books

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/books/` | List all books | Public |
| GET | `/api/books/{id}/` | Get book details | Public |
| POST | `/api/books/` | Create book | Admin |
| PUT | `/api/books/{id}/` | Update book | Admin |
| DELETE | `/api/books/{id}/` | Delete book | Admin |

### Borrowings

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/borrowings/` | List borrowings | Member (own) / Admin (all) |
| POST | `/api/borrowings/checkout/` | Checkout a book | Member |
| POST | `/api/borrowings/{id}/checkin/` | Return a book | Admin |
| GET | `/api/borrowings/current/` | Active borrowings | Member |
| GET | `/api/borrowings/history/` | Borrowing history | Member |
| GET | `/api/borrowings/overdue/` | Overdue list | Admin |

### Ratings

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/ratings/` | List all ratings | Public |
| POST | `/api/ratings/` | Submit rating | Member |
| GET | `/api/ratings/{id}/` | Get rating details | Public |
| PUT | `/api/ratings/{id}/` | Update rating | Owner/Admin |
| DELETE | `/api/ratings/{id}/` | Delete rating | Owner/Admin |
| GET | `/api/ratings/my_ratings/` | User's ratings | Member |

## 📖 API Documentation

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **OpenAPI JSON**: `/swagger.json`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest tests/integration/test_borrowings_api.py
```

## 🐳 Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the API at http://localhost:8001
```

## ☁️ Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed Railway deployment instructions.

## 📁 Project Structure

```
book-catalog-api/
├── apps/
│   ├── accounts/      # User authentication & authorization
│   ├── books/         # Book inventory management
│   ├── borrowings/    # Checkout & return system
│   ├── ratings/       # Book rating & reviews
│   └── core/          # Shared utilities & middleware
├── config/
│   ├── settings/      # Environment-specific settings
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI application
├── tests/
│   ├── unit/          # Unit tests
│   └── integration/   # API integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | dev-key |
| `DEBUG` | Debug mode | False |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `ALLOWED_HOSTS` | Allowed host domains | localhost |
| `CORS_ALLOWED_ORIGINS` | CORS whitelist | http://localhost:3000 |

## 📄 License

MIT License - see LICENSE file for details.
