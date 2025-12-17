#!/bin/bash
# Startup script for Railway deployment
# Handles migrations, seeding, and server startup

set -e

export PORT=${PORT:-8000}

echo "🚀 Starting Library Management System..."

# Run database migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Setup user groups (Administrators, Members)
echo "👥 Setting up user groups..."
python manage.py setup_groups

# Seed sample books (only if database is empty)
echo "📚 Seeding books..."
python manage.py seed_books

# Create admin user (only if not exists)
echo "🔐 Checking admin user..."
python manage.py shell -c "
from apps.accounts.models import User
from django.contrib.auth.models import Group

if not User.objects.filter(email='admin678@gmail.com').exists():
    admin = User.objects.create_superuser(
        email='admin678@gmail.com',
        password='Admin678@',
        username='admin678',
        first_name='System',
        last_name='Administrator'
    )
    admin_group, _ = Group.objects.get_or_create(name='Administrators')
    admin.groups.add(admin_group)
    print('✅ Admin user created successfully')
else:
    print('ℹ️ Admin user already exists')
"

# Start Gunicorn server
echo "🌐 Starting Gunicorn on port $PORT..."
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
