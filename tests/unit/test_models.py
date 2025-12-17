"""
Unit tests for models.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User
from apps.books.models import Book
from apps.borrowings.models import Borrowing
from apps.ratings.models import BookRating


@pytest.mark.django_db
class TestUserModel:
    """Tests for the User model."""

    def test_user_creation(self, member_group):
        """Test user can be created successfully."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123!'
        )
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.check_password('TestPass123!')
        assert user.is_active is True

    def test_user_str(self, member_user):
        """Test user string representation."""
        assert str(member_user) == 'member@bookcatalog.com'

    def test_is_administrator_property(self, admin_user, member_user):
        """Test is_administrator property."""
        assert admin_user.is_administrator is True
        assert member_user.is_administrator is False

    def test_is_member_property(self, admin_user, member_user):
        """Test is_member property."""
        assert member_user.is_member is True


@pytest.mark.django_db
class TestBookModel:
    """Tests for the Book model."""

    def test_book_creation(self):
        """Test book can be created successfully."""
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123'
        )
        assert book.title == 'Test Book'
        assert book.is_available is True

    def test_book_str(self, sample_book):
        """Test book string representation."""
        assert str(sample_book) == 'Clean Architecture by Robert Martin'

    def test_book_default_availability(self):
        """Test book is available by default."""
        book = Book.objects.create(
            title='New Book',
            author='Author',
            isbn='9876543210987'
        )
        assert book.is_available is True


@pytest.mark.django_db
class TestBorrowingModel:
    """Tests for the Borrowing model."""

    def test_borrowing_creation(self, member_user, sample_book):
        """Test borrowing can be created successfully."""
        borrowing = Borrowing.objects.create(
            user=member_user,
            book=sample_book
        )
        assert borrowing.user == member_user
        assert borrowing.book == sample_book
        assert borrowing.returned_at is None

    def test_borrowing_default_due_date(self, member_user, sample_book):
        """Test borrowing sets default due date."""
        borrowing = Borrowing.objects.create(
            user=member_user,
            book=sample_book
        )
        expected_due = timezone.now() + timedelta(days=14)
        # Allow 1 minute tolerance
        assert abs((borrowing.due_date - expected_due).total_seconds()) < 60

    def test_borrowing_is_active_property(self, member_user, sample_book):
        """Test is_active property."""
        borrowing = Borrowing.objects.create(
            user=member_user,
            book=sample_book
        )
        assert borrowing.is_active is True

        borrowing.returned_at = timezone.now()
        borrowing.save()
        assert borrowing.is_active is False

    def test_borrowing_is_overdue_property(self, member_user, sample_book):
        """Test is_overdue property."""
        borrowing = Borrowing.objects.create(
            user=member_user,
            book=sample_book,
            due_date=timezone.now() - timedelta(days=1)  # Due yesterday
        )
        assert borrowing.is_overdue is True

        borrowing.returned_at = timezone.now()
        borrowing.save()
        assert borrowing.is_overdue is False

    def test_borrowing_str(self, member_user, sample_book):
        """Test borrowing string representation."""
        borrowing = Borrowing.objects.create(
            user=member_user,
            book=sample_book
        )
        assert 'Active' in str(borrowing)

        borrowing.returned_at = timezone.now()
        borrowing.save()
        assert 'Returned' in str(borrowing)


@pytest.mark.django_db
class TestBookRatingModel:
    """Tests for the BookRating model."""

    def test_rating_creation(self, member_user, sample_book):
        """Test rating can be created successfully."""
        rating = BookRating.objects.create(
            user=member_user,
            book=sample_book,
            rating=5,
            comment='Great book!'
        )
        assert rating.rating == 5
        assert rating.comment == 'Great book!'

    def test_rating_str(self, member_user, sample_book):
        """Test rating string representation."""
        rating = BookRating.objects.create(
            user=member_user,
            book=sample_book,
            rating=4,
            comment='Good read'
        )
        assert '4/5' in str(rating)

    def test_rating_unique_constraint(self, member_user, sample_book):
        """Test user can only rate a book once."""
        BookRating.objects.create(
            user=member_user,
            book=sample_book,
            rating=5,
            comment='First rating'
        )
        with pytest.raises(Exception):  # IntegrityError
            BookRating.objects.create(
                user=member_user,
                book=sample_book,
                rating=3,
                comment='Second rating'
            )
