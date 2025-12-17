"""
Integration tests for authentication API.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestRegistrationAPI:
    """Tests for user registration."""

    def test_user_registration_success(self, api_client, member_group):
        """Test successful user registration."""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert 'user' in response.data
        assert response.data['user']['email'] == 'newuser@example.com'

    def test_user_registration_password_mismatch(self, api_client):
        """Test registration fails with mismatched passwords."""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_user_registration_duplicate_email(self, api_client, member_user):
        """Test registration fails with duplicate email."""
        url = reverse('register')
        data = {
            'email': member_user.email,
            'username': 'another',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Another',
            'last_name': 'User'
        }
        response = api_client.post(url, data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestLoginAPI:
    """Tests for user login."""

    def test_login_success(self, api_client, member_user):
        """Test successful login returns tokens."""
        url = reverse('login')
        data = {
            'email': 'member@bookcatalog.com',
            'password': 'MemberPass123!'
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_credentials(self, api_client, member_user):
        """Test login fails with invalid credentials."""
        url = reverse('login')
        data = {
            'email': 'member@bookcatalog.com',
            'password': 'WrongPassword!'
        }
        response = api_client.post(url, data)
        assert response.status_code == 401


@pytest.mark.django_db
class TestProfileAPI:
    """Tests for user profile."""

    def test_get_profile_authenticated(self, authenticated_member_client, member_user):
        """Test authenticated user can get their profile."""
        url = reverse('profile')
        response = authenticated_member_client.get(url)
        assert response.status_code == 200
        assert response.data['email'] == member_user.email

    def test_get_profile_unauthenticated(self, api_client):
        """Test unauthenticated request is rejected."""
        url = reverse('profile')
        response = api_client.get(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestAuthorizationAPI:
    """Tests for role-based authorization."""

    def test_admin_can_list_users(self, authenticated_admin_client):
        """Test admin can access user list."""
        url = reverse('user-list')
        response = authenticated_admin_client.get(url)
        assert response.status_code == 200

    def test_member_cannot_list_users(self, authenticated_member_client):
        """Test member cannot access user list."""
        url = reverse('user-list')
        response = authenticated_member_client.get(url)
        assert response.status_code == 403

    def test_anonymous_cannot_list_users(self, api_client):
        """Test anonymous user cannot access user list."""
        url = reverse('user-list')
        response = api_client.get(url)
        assert response.status_code == 401
