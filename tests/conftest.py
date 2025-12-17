"""
Pytest configuration and fixtures.
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from apps.accounts.models import User
from apps.books.models import Book


@pytest.fixture
def api_client():
    """Return an API client for making requests."""
    return APIClient()


@pytest.fixture
def admin_group(db):
    """Create and return the Administrators group."""
    group, _ = Group.objects.get_or_create(name='Administrators')
    return group


@pytest.fixture
def member_group(db):
    """Create and return the Members group."""
    group, _ = Group.objects.get_or_create(name='Members')
    return group


@pytest.fixture
def admin_user(db, admin_group):
    """Create and return an administrator user."""
    user = User.objects.create_user(
        email='admin@bookcatalog.com',
        username='admin',
        password='AdminPass123!'
    )
    user.groups.add(admin_group)
    return user


@pytest.fixture
def member_user(db, member_group):
    """Create and return a member user."""
    user = User.objects.create_user(
        email='member@bookcatalog.com',
        username='member',
        password='MemberPass123!'
    )
    user.groups.add(member_group)
    return user


@pytest.fixture
def another_member_user(db, member_group):
    """Create and return another member user."""
    user = User.objects.create_user(
        email='another@bookcatalog.com',
        username='another',
        password='AnotherPass123!'
    )
    user.groups.add(member_group)
    return user


@pytest.fixture
def authenticated_admin_client(admin_user):
    """Return an API client authenticated as admin."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def authenticated_member_client(member_user):
    """Return an API client authenticated as member."""
    client = APIClient()
    client.force_authenticate(user=member_user)
    return client


@pytest.fixture
def sample_book(db):
    """Create and return a sample available book."""
    return Book.objects.create(
        title='Clean Architecture',
        author='Robert Martin',
        isbn='9780134494166',
        description='Software design principles and patterns',
        page_count=432,
        genre='Technology',
        is_available=True
    )


@pytest.fixture
def another_book(db):
    """Create and return another sample book."""
    return Book.objects.create(
        title='The Pragmatic Programmer',
        author='David Thomas',
        isbn='9780135957059',
        description='From journeyman to master',
        page_count=352,
        genre='Technology',
        is_available=True
    )


@pytest.fixture
def unavailable_book(db):
    """Create and return an unavailable book."""
    return Book.objects.create(
        title='Code Complete',
        author='Steve McConnell',
        isbn='9780735619678',
        description='A practical handbook of software construction',
        page_count=960,
        genre='Technology',
        is_available=False
    )
