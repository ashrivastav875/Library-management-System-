# 🛡️ Security Documentation

This document outlines the security measures implemented in the Library Management System.

## Overview

The application follows OWASP security guidelines and Django security best practices to protect against common web vulnerabilities.

## Protection Mechanisms

### 1. SQL Injection Prevention

**Risk**: Attackers inject malicious SQL through user inputs.

**Protection**: 
- All database queries use Django ORM with parameterized queries
- No raw SQL queries in the codebase
- Input validation on all user-supplied data

```python
# Safe - parameterized query
Book.objects.filter(title__icontains=user_input)

# Never used - vulnerable to injection
# cursor.execute(f"SELECT * FROM books WHERE title = '{user_input}'")
```

### 2. Cross-Site Scripting (XSS) Prevention

**Risk**: Attackers inject malicious scripts into web pages.

**Protection**:
- `X-XSS-Protection: 1; mode=block` header
- `X-Content-Type-Options: nosniff` prevents MIME sniffing
- Django's template auto-escaping (for admin pages)
- JSON responses only (no HTML rendering in API)

### 3. Cross-Site Request Forgery (CSRF) Protection

**Risk**: Attackers trick users into performing unintended actions.

**Protection**:
- Django CSRF middleware enabled
- `CSRF_COOKIE_SECURE = True` in production
- JWT tokens for API authentication (stateless)

### 4. Clickjacking Protection

**Risk**: Attackers embed the site in iframes to hijack clicks.

**Protection**:
- `X-Frame-Options: DENY` header
- Configured via Django's `XFrameOptionsMiddleware`

### 5. Authentication Security

**Protection**:
- JWT tokens with configurable expiration (60 min access, 7 days refresh)
- Password validation (length, complexity, common passwords)
- Secure password hashing (PBKDF2 with SHA256)
- Token rotation on refresh

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 6. HTTPS Enforcement

**Production Settings**:
```python
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 7. HTTP Strict Transport Security (HSTS)

**Protection**: Forces browsers to only use HTTPS for 1 year.

```python
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 8. Custom Security Headers

The `SecurityHeadersMiddleware` adds additional protection:

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `X-XSS-Protection` | `1; mode=block` | Enable XSS filter |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Control referrer info |
| `Permissions-Policy` | Restricted | Disable unused browser features |
| `Cache-Control` | `no-store` | Prevent caching of API responses |

## Input Validation

All user inputs are validated:

- **ISBN**: Exact 13-digit format
- **Email**: RFC-compliant validation
- **Rating**: 1-5 integer range
- **Passwords**: Minimum length, complexity requirements

## Authorization Model

Role-based access control using Django Groups:

| Role | Permissions |
|------|-------------|
| **Anonymous** | Read books, read ratings |
| **Member** | + Checkout books, submit ratings |
| **Administrator** | + CRUD books, checkin books, view all data |

## Secure Defaults

- `DEBUG = False` in production
- `SECRET_KEY` loaded from environment variable
- `ALLOWED_HOSTS` explicitly configured
- CORS restricted to specific origins

## Security Audit Checklist

Before deployment, verify:

- [ ] Secret key is unique and not committed to git
- [ ] Debug mode is disabled
- [ ] Database credentials are environment variables
- [ ] HTTPS is enforced
- [ ] Admin URL is not publicly known
- [ ] Default passwords are changed
- [ ] Logging is configured for security events
- [ ] Dependencies are up to date (`pip list --outdated`)

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it to:
- Email: security@bookcatalog.com
- Do NOT create public GitHub issues for security problems
