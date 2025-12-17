"""
Management command to rebuild search vectors for all books.
Run this after migrating to PostgreSQL or when search isn't working.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Rebuild search vectors for all books (PostgreSQL FTS)'

    def handle(self, *args, **options):
        from apps.books.models import Book
        
        self.stdout.write('Rebuilding search vectors...')
        
        try:
            # Use raw SQL for rebuilding search vectors
            from django.db import connection
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE books SET search_vector = 
                        setweight(to_tsvector('english', COALESCE(title, '')), 'A') ||
                        setweight(to_tsvector('english', COALESCE(author, '')), 'A') ||
                        setweight(to_tsvector('english', COALESCE(isbn, '')), 'B') ||
                        setweight(to_tsvector('english', COALESCE(genre, '')), 'B') ||
                        setweight(to_tsvector('english', COALESCE(description, '')), 'C')
                """)
            
            count = Book.objects.count()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully rebuilt search vectors for {count} books!'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error rebuilding search vectors: {e}'
            ))
            self.stdout.write(self.style.WARNING(
                'This command requires PostgreSQL with pg_trgm extension.'
            ))
