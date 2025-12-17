"""
URL configuration for Book Catalog System.

Provides API endpoints for book management, borrowings, and ratings.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Book Catalog API",
        default_version='v1',
        description="""
RESTful API for managing a book catalog system.

## Features
- **Books**: Browse, search, and manage book inventory
- **Borrowings**: Checkout and return books with due date tracking  
- **Ratings**: Rate and review books

## Authentication
All write operations require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```
        """,
        contact=openapi.Contact(email="support@bookcatalog.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Root redirect to API documentation
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'),
    
    # Admin panel
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('apps.accounts.urls')),
    path('api/', include('apps.books.urls')),
    path('api/', include('apps.borrowings.urls')),
    path('api/', include('apps.ratings.urls')),

    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]
