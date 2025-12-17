# 🚀 Deployment Guide

Complete guide for deploying the Library Management System to Railway.

## Prerequisites

- [Railway account](https://railway.app)
- [GitHub account](https://github.com) with this repository pushed
- PostgreSQL database (provided by Railway)

## Deployment Steps

### 1. Create Railway Project

1. Log in to [Railway](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect your GitHub account and select this repository

### 2. Add PostgreSQL Database

1. In your Railway project, click **"New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically provision the database

### 3. Configure Environment Variables

In Railway, go to your web service → **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `SECRET_KEY` | Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | Your Railway domain (e.g., `your-app.up.railway.app`) |
| `CORS_ALLOWED_ORIGINS` | `*` or specific domains |

> **Note**: `DATABASE_URL` is automatically injected by Railway when you link the PostgreSQL service.

### 4. Link Database to Web Service

1. Click on your web service
2. Go to **Variables** tab
3. Click **"Add Reference"**
4. Select your PostgreSQL service
5. This adds `DATABASE_URL` automatically

### 5. Deploy

Railway will automatically:
1. Build the Docker image
2. Run migrations via `start.sh`
3. Create admin user
4. Seed sample books
5. Start Gunicorn server

## Startup Script (`start.sh`)

The deployment runs this script automatically:

```bash
#!/bin/bash
export PORT=${PORT:-8000}

# Run migrations
python manage.py migrate --noinput

# Setup user groups
python manage.py setup_groups

# Seed books (only if database is empty)
python manage.py seed_books

# Create admin user (only if not exists)
python manage.py shell -c "
from apps.accounts.models import User
from django.contrib.auth.models import Group

if not User.objects.filter(email='admin@bookcatalog.com').exists():
    admin = User.objects.create_superuser(
        email='admin@bookcatalog.com',
        password='Admin@123',
        username='admin',
        first_name='Admin',
        last_name='User'
    )
    admin_group, _ = Group.objects.get_or_create(name='Administrators')
    admin.groups.add(admin_group)
    print('Admin user created')
else:
    print('Admin user already exists')
"

# Start server
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

## Verify Deployment

After deployment, verify these URLs work:

| URL | Expected |
|-----|----------|
| `https://your-app.up.railway.app/` | Redirects to Swagger |
| `https://your-app.up.railway.app/swagger/` | API Documentation |
| `https://your-app.up.railway.app/api/books/` | Book list (JSON) |
| `https://your-app.up.railway.app/admin/` | Django Admin Panel |

## Troubleshooting

### Database Connection Errors

If you see `could not translate host name`:
1. Verify PostgreSQL service is running
2. Check if `DATABASE_URL` is correctly linked
3. Restart the web service

### Worker Timeout

If you see `WORKER TIMEOUT`:
1. Check Railway metrics for memory usage
2. Consider upgrading Railway plan
3. Optimize database queries

### Static Files Not Loading

Ensure `whitenoise` is in requirements and middleware is configured:

```python
MIDDLEWARE = [
    ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

## Security Checklist

Before going live, verify:

- [ ] `DEBUG = False`
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` restricted to your domain
- [ ] `CORS_ALLOWED_ORIGINS` restricted (not `*`)
- [ ] Admin password changed from default
- [ ] HTTPS enforced (Railway does this automatically)

## Monitoring

Railway provides:
- **Logs**: View in real-time from the dashboard
- **Metrics**: CPU and memory usage
- **Deployments**: Rollback to previous versions if needed
