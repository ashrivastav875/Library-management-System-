"""
Migration to enable PostgreSQL pg_trgm extension for trigram similarity search.
"""
from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
    ]
