"""
Django settings package.
Uses environment-based settings loading.
"""
import os

environment = os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Default to development settings
if 'production' in environment:
    from .production import *
elif 'testing' in environment:
    from .testing import *
else:
    from .development import *
