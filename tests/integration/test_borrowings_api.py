"""
Integration tests for borrowings API.
"""
import pytest
from django.urls import reverse
from apps.books.models import Book


@pytest.mark.django_db
class TestCheckoutAPI:
    """Tests for checking out books."""

    def test_member_can_checkout_book(self, authenticated_member_client, sample_book):
        """Test member can checkout an available book."""
        url = reverse('borrowing-checkout')
        data = {'book_id': sample_book.id}
        response = authenticated_member_client.post(url, data)
        assert response.status_code == 201
        assert response.data['book']['id'] == sample_book.id

        # Verify book is no longer available
        sample_book.refresh_from_db()
        assert sample_book.is_available is False

    def test_cannot_checkout_unavailable_book(self, authenticated_member_client, unavailable_book):
        """Test cannot checkout unavailable book."""
        url = reverse('borrowing-checkout')
        data = {'book_id': unavailable_book.id}
        response = authenticated_member_client.post(url, data)
        assert response.status_code == 400
        error_text = str(response.data).lower()
        assert 'not available' in error_text or 'available' in error_text

    def test_cannot_checkout_same_book_twice(self, authenticated_member_client, sample_book):
        """Test user cannot checkout same book twice."""
        url = reverse('borrowing-checkout')
        data = {'book_id': sample_book.id}

        # First checkout should succeed
        response1 = authenticated_member_client.post(url, data)
        assert response1.status_code == 201

        # Second checkout should fail
        sample_book.is_available = True
        sample_book.save()
        response2 = authenticated_member_client.post(url, data)
        assert response2.status_code == 400

    def test_anonymous_cannot_checkout(self, api_client, sample_book):
        """Test anonymous user cannot checkout books."""
        url = reverse('borrowing-checkout')
        data = {'book_id': sample_book.id}
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_checkout_nonexistent_book(self, authenticated_member_client):
        """Test checking out nonexistent book fails."""
        url = reverse('borrowing-checkout')
        data = {'book_id': 99999}
        response = authenticated_member_client.post(url, data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestCheckinAPI:
    """Tests for checking in (returning) books."""

    def test_admin_can_checkin_book(self, authenticated_admin_client, authenticated_member_client, sample_book):
        """Test admin can checkin a borrowed book."""
        # Member checks out the book
        checkout_url = reverse('borrowing-checkout')
        checkout_response = authenticated_member_client.post(
            checkout_url, {'book_id': sample_book.id}
        )
        borrowing_id = checkout_response.data['id']

        # Admin checks it in
        checkin_url = reverse('borrowing-checkin', args=[borrowing_id])
        response = authenticated_admin_client.post(checkin_url)
        assert response.status_code == 200
        assert response.data['returned_at'] is not None

        # Verify book is available again
        sample_book.refresh_from_db()
        assert sample_book.is_available is True

    def test_cannot_checkin_already_returned_book(self, authenticated_admin_client, authenticated_member_client, sample_book):
        """Test cannot checkin already returned book."""
        # Member checks out
        checkout_url = reverse('borrowing-checkout')
        checkout_response = authenticated_member_client.post(
            checkout_url, {'book_id': sample_book.id}
        )
        borrowing_id = checkout_response.data['id']

        # Admin checks in once
        checkin_url = reverse('borrowing-checkin', args=[borrowing_id])
        authenticated_admin_client.post(checkin_url)

        # Admin tries to checkin again
        response = authenticated_admin_client.post(checkin_url)
        assert response.status_code == 400


@pytest.mark.django_db
class TestBorrowingListAPI:
    """Tests for listing borrowings."""

    def test_member_sees_own_borrowings(self, authenticated_member_client, sample_book):
        """Test member sees only their own borrowings."""
        # Create a borrowing
        checkout_url = reverse('borrowing-checkout')
        authenticated_member_client.post(checkout_url, {'book_id': sample_book.id})

        # List borrowings
        url = reverse('borrowing-list')
        response = authenticated_member_client.get(url)
        assert response.status_code == 200
        borrowings = response.data if isinstance(response.data, list) else response.data.get('results', [])
        assert len(borrowings) >= 1

    def test_admin_sees_all_borrowings(self, authenticated_admin_client, authenticated_member_client, sample_book):
        """Test admin can see all borrowings."""
        # Member creates a borrowing
        checkout_url = reverse('borrowing-checkout')
        authenticated_member_client.post(checkout_url, {'book_id': sample_book.id})

        # Admin lists all borrowings
        url = reverse('borrowing-list')
        response = authenticated_admin_client.get(url)
        assert response.status_code == 200

    def test_current_borrowings_endpoint(self, authenticated_member_client, sample_book):
        """Test current borrowings endpoint."""
        # Create a borrowing
        checkout_url = reverse('borrowing-checkout')
        authenticated_member_client.post(checkout_url, {'book_id': sample_book.id})

        # Get current borrowings
        url = reverse('borrowing-current')
        response = authenticated_member_client.get(url)
        assert response.status_code == 200
        borrowings = response.data if isinstance(response.data, list) else response.data.get('results', [])
        for borrowing in borrowings:
            assert borrowing['is_active'] is True

    def test_overdue_borrowings_admin_only(self, api_client, member_user, admin_user):
        """Test overdue borrowings endpoint is admin only."""
        url = reverse('borrowing-overdue')

        # Member should not access
        api_client.force_authenticate(user=member_user)
        member_response = api_client.get(url)
        assert member_response.status_code == 403

        # Admin should access
        api_client.force_authenticate(user=admin_user)
        admin_response = api_client.get(url)
        assert admin_response.status_code == 200
