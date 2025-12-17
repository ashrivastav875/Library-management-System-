"""
Integration tests for books API.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestBooksListAPI:
    """Tests for books listing."""

    def test_list_books_anonymous(self, api_client, sample_book, another_book):
        """Test anonymous users can list books."""
        url = reverse('book-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 2

    def test_list_books_with_search(self, api_client, sample_book, another_book):
        """Test search functionality."""
        url = reverse('book-list')
        response = api_client.get(url, {'search': 'Architecture'})
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Clean Architecture'

    def test_list_books_filter_available(self, api_client, sample_book, unavailable_book):
        """Test filtering by availability."""
        url = reverse('book-list')
        response = api_client.get(url, {'is_available': 'true'})
        assert response.status_code == 200
        # Only available books
        for book in response.data['results']:
            assert book['is_available'] is True


@pytest.mark.django_db
class TestBookDetailAPI:
    """Tests for book detail view."""

    def test_get_book_detail(self, api_client, sample_book):
        """Test getting book details."""
        url = reverse('book-detail', args=[sample_book.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['title'] == sample_book.title
        assert response.data['author'] == sample_book.author

    def test_get_nonexistent_book(self, api_client):
        """Test getting nonexistent book returns 404."""
        url = reverse('book-detail', args=[99999])
        response = api_client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestBookCreateAPI:
    """Tests for book creation."""

    def test_admin_can_create_book(self, authenticated_admin_client):
        """Test admin can create books."""
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '1234567890123',
            'description': 'A new book',
            'page_count': 200,
            'genre': 'Fiction'
        }
        response = authenticated_admin_client.post(url, data)
        assert response.status_code == 201

    def test_member_cannot_create_book(self, authenticated_member_client):
        """Test member cannot create books."""
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '1234567890123'
        }
        response = authenticated_member_client.post(url, data)
        assert response.status_code == 403

    def test_anonymous_cannot_create_book(self, api_client):
        """Test anonymous user cannot create books."""
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '1234567890123'
        }
        response = api_client.post(url, data)
        assert response.status_code == 401


@pytest.mark.django_db
class TestBookUpdateAPI:
    """Tests for book update."""

    def test_admin_can_update_book(self, authenticated_admin_client, sample_book):
        """Test admin can update books."""
        url = reverse('book-detail', args=[sample_book.id])
        data = {'title': 'Updated Title'}
        response = authenticated_admin_client.patch(url, data)
        assert response.status_code == 200

    def test_member_cannot_update_book(self, authenticated_member_client, sample_book):
        """Test member cannot update books."""
        url = reverse('book-detail', args=[sample_book.id])
        data = {'title': 'Updated Title'}
        response = authenticated_member_client.patch(url, data)
        assert response.status_code == 403


@pytest.mark.django_db
class TestBookDeleteAPI:
    """Tests for book deletion."""

    def test_admin_can_delete_book(self, authenticated_admin_client, sample_book):
        """Test admin can delete books."""
        url = reverse('book-detail', args=[sample_book.id])
        response = authenticated_admin_client.delete(url)
        assert response.status_code == 204

    def test_member_cannot_delete_book(self, authenticated_member_client, sample_book):
        """Test member cannot delete books."""
        url = reverse('book-detail', args=[sample_book.id])
        response = authenticated_member_client.delete(url)
        assert response.status_code == 403
