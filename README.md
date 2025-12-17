# 📚 Library Management System

A comprehensive RESTful API for library management where users can search for books and borrow them, built with Django REST Framework.

## 🌐 Live Demo

| Link | URL |
|------|-----|
| � **Swagger UI** | [https://web-production-12f57.up.railway.app/swagger/](https://web-production-12f57.up.railway.app/swagger/) |
| 📚 **ReDoc** | [https://web-production-12f57.up.railway.app/redoc/](https://web-production-12f57.up.railway.app/redoc/) |
| ⚙️ **Admin Panel** | [https://web-production-12f57.up.railway.app/admin/](https://web-production-12f57.up.railway.app/admin/) |
| 📡 **API Base** | [https://web-production-12f57.up.railway.app/api/](https://web-production-12f57.up.railway.app/api/) |

**Admin Credentials**: `admin678@gmail.com` / `Admin678@`

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| User Roles (Anonymous, Member, Admin) | ✅ | Django Groups + Custom Permissions |
| User Registration & Login | ✅ | JWT Authentication (SimpleJWT) |
| Extended User Model | ✅ | `apps/accounts/models.py` |
| Book Model | ✅ | Title, Author, ISBN, Page Count, Availability |
| Loan Model | ✅ | Borrowing with User, Book, Dates |
| Borrow/Return Endpoints | ✅ | POST checkout, POST checkin |
| Unit Tests | ✅ | 49 tests (models, views) |
| Integration Tests | ✅ | API endpoint tests |
| Swagger Documentation | ✅ | drf-yasg with Swagger UI |
| PostgreSQL Ready | ✅ | Django + psycopg2 |
| Dockerfile | ✅ | Multi-stage build |
| Filtering & Pagination | ✅ | django-filter + REST pagination |
| Security (CSRF, XSS, SQL Injection) | ✅ | Custom middleware + Django security |

## ✨ Features

- **📖 Book Management**: Full CRUD operations for book inventory
- **🔍 Advanced Search**: PostgreSQL full-text search with typo tolerance (pg_trgm)
- **📋 Borrowing System**: Borrow and return books with due date tracking
- **⭐ Rating System**: Rate and review books (1-5 stars)
- **🔐 JWT Authentication**: Secure token-based authentication
- **👥 Role-Based Access**: Administrators and Members with different permissions
- **📄 API Documentation**: Interactive Swagger UI and ReDoc
- **🛡️ Security Headers**: Custom middleware for XSS, Clickjacking protection

## 🛡️ Security Features

| Protection | Implementation |
|------------|----------------|
| **SQL Injection** | Django ORM with parameterized queries |
| **XSS** | Content-Type sniffing prevention, X-XSS-Protection headers |
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
cd library-management-system

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

### Default Admin Credentials (Production)

- **Email**: `admin678@gmail.com`
- **Password**: `Admin678@`

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
| GET | `/api/books/` | List all books (with search, filter, pagination) | Public |
| GET | `/api/books/{id}/` | Get book details | Public |
| POST | `/api/books/` | Create book | Admin |
| PUT | `/api/books/{id}/` | Update book | Admin |
| DELETE | `/api/books/{id}/` | Delete book | Admin |

### Borrowings (Loans)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/borrowings/` | List borrowings | Member (own) / Admin (all) |
| POST | `/api/borrowings/checkout/` | Borrow a book | Member |
| POST | `/api/borrowings/{id}/checkin/` | Return a book | Admin |
| GET | `/api/borrowings/current/` | Active borrowings | Member |
| GET | `/api/borrowings/history/` | Borrowing history | Member |
| GET | `/api/borrowings/overdue/` | Overdue list | Admin |

### Ratings

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/ratings/` | List all ratings | Public |
| POST | `/api/ratings/` | Submit rating | Member |
| GET | `/api/ratings/my_ratings/` | User's ratings | Member |

## 📖 API Documentation

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **OpenAPI JSON**: `/swagger.json`

## 🧪 Testing

```bash
# Run all tests (49 tests)
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest tests/integration/test_borrowings_api.py
```

### Test Coverage

- **Unit Tests**: User, Book, Borrowing, BookRating models
- **Integration Tests**: Authentication, Books API, Borrowings API

## 🐳 Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the API at http://localhost:8001
```

## ☁️ Deployment

The project is configured for Railway deployment. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (False in production) | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `ALLOWED_HOSTS` | Allowed host domains | Yes |
| `DJANGO_SETTINGS_MODULE` | Settings module | Yes |

## 📁 Project Structure

```
library-management-system/
├── apps/
│   ├── accounts/      # User authentication & authorization
│   ├── books/         # Book inventory with search
│   ├── borrowings/    # Loan tracking system
│   ├── ratings/       # Book ratings & reviews
│   └── core/          # Security middleware
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
├── start.sh           # Production startup script
└── README.md
```

## 🔧 Technologies Used

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL with full-text search (pg_trgm)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Testing**: Pytest with Django plugin
- **Deployment**: Docker, Railway/Heroku ready

## 📄 License

MIT License
