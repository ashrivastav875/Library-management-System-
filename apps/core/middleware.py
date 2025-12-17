"""
Security middleware for enhanced protection.

Adds security headers to all responses for protection against:
- XSS (Cross-Site Scripting)
- Clickjacking
- MIME type sniffing
- Information disclosure
"""
from typing import Callable
from django.http import HttpRequest, HttpResponse


class SecurityHeadersMiddleware:
    """
    Middleware that adds security headers to all HTTP responses.
    
    Headers added:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - X-XSS-Protection: 1; mode=block
    - Referrer-Policy: strict-origin-when-cross-origin
    - Permissions-Policy: Restricts browser features
    - Cache-Control: For sensitive endpoints
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Enable XSS filter in browsers
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Control referrer information
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Restrict browser features
        response['Permissions-Policy'] = (
            'accelerometer=(), '
            'camera=(), '
            'geolocation=(), '
            'gyroscope=(), '
            'magnetometer=(), '
            'microphone=(), '
            'payment=(), '
            'usb=()'
        )
        
        # Add cache control for API responses
        if request.path.startswith('/api/'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
        
        return response


class RequestLoggingMiddleware:
    """
    Middleware for logging API requests (useful for debugging/monitoring).
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Log request info (can be extended with proper logging)
        response = self.get_response(request)
        return response
