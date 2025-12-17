"""
Management command to seed sample books into the catalog.
"""
from django.core.management.base import BaseCommand
from apps.books.models import Book
from datetime import date
import random


class Command(BaseCommand):
    help = 'Populate the catalog with sample books'

    def handle(self, *args, **options):
        self.stdout.write('📚 Populating book catalog...\n')

        # Completely different book collection organized by category
        catalog = {
            'Technology': [
                ('Clean Architecture', 'Robert Martin', 'Software design principles and patterns'),
                ('The Pragmatic Programmer', 'David Thomas', 'From journeyman to master'),
                ('Code Complete', 'Steve McConnell', 'A practical handbook of software construction'),
                ('Design Patterns', 'Gang of Four', 'Elements of reusable object-oriented software'),
                ('Refactoring', 'Martin Fowler', 'Improving the design of existing code'),
                ('Domain-Driven Design', 'Eric Evans', 'Tackling complexity in software'),
                ('The Mythical Man-Month', 'Frederick Brooks', 'Essays on software engineering'),
                ('Working Effectively with Legacy Code', 'Michael Feathers', 'Change code safely'),
                ('Continuous Delivery', 'Jez Humble', 'Reliable software releases'),
                ('Site Reliability Engineering', 'Google SRE Team', 'How Google runs production systems'),
            ],
            'Business': [
                ('Zero to One', 'Peter Thiel', 'Notes on startups and how to build the future'),
                ('The Lean Startup', 'Eric Ries', 'How entrepreneurs use continuous innovation'),
                ('Good to Great', 'Jim Collins', 'Why some companies make the leap'),
                ('Start with Why', 'Simon Sinek', 'How great leaders inspire action'),
                ('The Hard Thing About Hard Things', 'Ben Horowitz', 'Building a business when there are no easy answers'),
                ('Shoe Dog', 'Phil Knight', 'A memoir by the creator of Nike'),
                ('Principles', 'Ray Dalio', 'Life and work principles'),
                ('The Innovator Dilemma', 'Clayton Christensen', 'When new technologies cause great firms to fail'),
                ('Blue Ocean Strategy', 'W. Chan Kim', 'Creating uncontested market space'),
                ('Built to Last', 'Jim Collins', 'Successful habits of visionary companies'),
            ],
            'Psychology': [
                ('Influence', 'Robert Cialdini', 'The psychology of persuasion'),
                ('Predictably Irrational', 'Dan Ariely', 'Hidden forces that shape our decisions'),
                ('The Power of Habit', 'Charles Duhigg', 'Why we do what we do in life and business'),
                ('Emotional Intelligence', 'Daniel Goleman', 'Why it can matter more than IQ'),
                ('Flow', 'Mihaly Csikszentmihalyi', 'The psychology of optimal experience'),
                ('Drive', 'Daniel Pink', 'The surprising truth about what motivates us'),
                ('Quiet', 'Susan Cain', 'The power of introverts in a world that cant stop talking'),
                ('The Paradox of Choice', 'Barry Schwartz', 'Why more is less'),
                ('Stumbling on Happiness', 'Daniel Gilbert', 'Why we struggle to predict happiness'),
                ('Switch', 'Chip Heath', 'How to change things when change is hard'),
            ],
            'History': [
                ('Guns, Germs, and Steel', 'Jared Diamond', 'The fates of human societies'),
                ('A Short History of Nearly Everything', 'Bill Bryson', 'Science and history explained'),
                ('The Silk Roads', 'Peter Frankopan', 'A new history of the world'),
                ('Team of Rivals', 'Doris Kearns Goodwin', 'Lincoln and his cabinet'),
                ('The Rise and Fall of the Third Reich', 'William Shirer', 'A history of Nazi Germany'),
                ('1776', 'David McCullough', 'The year that transformed America'),
                ('The Wright Brothers', 'David McCullough', 'The dramatic story of aviation pioneers'),
                ('Dead Wake', 'Erik Larson', 'The last crossing of the Lusitania'),
                ('The Devil in the White City', 'Erik Larson', 'Murder and magic at the 1893 Chicago fair'),
                ('SPQR', 'Mary Beard', 'A history of ancient Rome'),
            ],
            'Philosophy': [
                ('Meditations', 'Marcus Aurelius', 'Stoic philosophy from a Roman emperor'),
                ('Beyond Good and Evil', 'Friedrich Nietzsche', 'Prelude to a philosophy of the future'),
                ('The Republic', 'Plato', 'Justice and the ideal state'),
                ('Tao Te Ching', 'Lao Tzu', 'The book of the way'),
                ('Ethics', 'Baruch Spinoza', 'A geometric method of philosophy'),
                ('Being and Time', 'Martin Heidegger', 'Fundamental ontology'),
                ('Critique of Pure Reason', 'Immanuel Kant', 'The limits of human knowledge'),
                ('The Art of War', 'Sun Tzu', 'Ancient military strategy'),
                ('Letters from a Stoic', 'Seneca', 'Practical wisdom for modern life'),
                ('The Problems of Philosophy', 'Bertrand Russell', 'An introduction to philosophy'),
            ],
            'Science': [
                ('A Brief History of Time', 'Stephen Hawking', 'From the Big Bang to black holes'),
                ('The Selfish Gene', 'Richard Dawkins', 'Evolution and the gene'),
                ('Cosmos', 'Carl Sagan', 'A personal voyage through the universe'),
                ('The Origin of Species', 'Charles Darwin', 'The foundation of evolutionary biology'),
                ('Silent Spring', 'Rachel Carson', 'The environmental movement begins'),
                ('The Structure of Scientific Revolutions', 'Thomas Kuhn', 'How science progresses'),
                ('The Elegant Universe', 'Brian Greene', 'String theory explained'),
                ('The Double Helix', 'James Watson', 'Discovery of DNA structure'),
                ('Surely You re Joking Mr Feynman', 'Richard Feynman', 'Adventures of a curious character'),
                ('Pale Blue Dot', 'Carl Sagan', 'A vision of the human future in space'),
            ],
            'Economics': [
                ('Freakonomics', 'Steven Levitt', 'A rogue economist explores the hidden side'),
                ('The Wealth of Nations', 'Adam Smith', 'The foundation of modern economics'),
                ('Capital in the Twenty-First Century', 'Thomas Piketty', 'Wealth and inequality'),
                ('Thinking Strategically', 'Avinash Dixit', 'The competitive edge in business'),
                ('Nudge', 'Richard Thaler', 'Improving decisions about health and happiness'),
                ('The Undercover Economist', 'Tim Harford', 'Exposing why the rich are rich'),
                ('Poor Economics', 'Abhijit Banerjee', 'A radical rethinking of the fight against poverty'),
                ('Animal Spirits', 'George Akerlof', 'How human psychology drives the economy'),
                ('The Black Swan', 'Nassim Taleb', 'The impact of the highly improbable'),
                ('Misbehaving', 'Richard Thaler', 'The making of behavioral economics'),
            ],
            'Health': [
                ('Why We Sleep', 'Matthew Walker', 'Unlocking the power of sleep and dreams'),
                ('The Body', 'Bill Bryson', 'A guide for occupants'),
                ('How Not to Die', 'Michael Greger', 'Foods that prevent and reverse disease'),
                ('Born to Run', 'Christopher McDougall', 'A hidden tribe and ultra runners'),
                ('Breath', 'James Nestor', 'The new science of a lost art'),
                ('The China Study', 'T. Colin Campbell', 'The most comprehensive study of nutrition'),
                ('In Defense of Food', 'Michael Pollan', 'An eater manifesto'),
                ('Brain Rules', 'John Medina', '12 principles for surviving and thriving'),
                ('Spark', 'John Ratey', 'The revolutionary new science of exercise'),
                ('The Immune System Recovery Plan', 'Susan Blum', 'A doctor program'),
            ],
            'Creativity': [
                ('Steal Like an Artist', 'Austin Kleon', '10 things nobody told you about being creative'),
                ('The War of Art', 'Steven Pressfield', 'Break through the blocks'),
                ('Big Magic', 'Elizabeth Gilbert', 'Creative living beyond fear'),
                ('Show Your Work', 'Austin Kleon', '10 ways to share your creativity'),
                ('The Artists Way', 'Julia Cameron', 'A spiritual path to higher creativity'),
                ('Originals', 'Adam Grant', 'How non-conformists move the world'),
                ('Creative Confidence', 'Tom Kelley', 'Unleashing creative potential'),
                ('Creativity Inc', 'Ed Catmull', 'Overcoming the unseen forces'),
                ('The Creative Habit', 'Twyla Tharp', 'Learn it and use it for life'),
                ('Imagine', 'Jonah Lehrer', 'How creativity works'),
            ],
            'Leadership': [
                ('Leaders Eat Last', 'Simon Sinek', 'Why some teams pull together'),
                ('Extreme Ownership', 'Jocko Willink', 'How Navy SEALs lead and win'),
                ('The Five Dysfunctions of a Team', 'Patrick Lencioni', 'A leadership fable'),
                ('Dare to Lead', 'Brene Brown', 'Brave work tough conversations whole hearts'),
                ('Radical Candor', 'Kim Scott', 'Be a kickass boss without losing humanity'),
                ('The Culture Code', 'Daniel Coyle', 'The secrets of highly successful groups'),
                ('Multipliers', 'Liz Wiseman', 'How the best leaders make everyone smarter'),
                ('Turn the Ship Around', 'David Marquet', 'A true story of turning followers into leaders'),
                ('Primal Leadership', 'Daniel Goleman', 'Unleashing the power of emotional intelligence'),
                ('The Making of a Manager', 'Julie Zhuo', 'What to do when everyone looks to you'),
            ],
        }

        created_count = 0
        total_books = sum(len(books) for books in catalog.values())
        current = 0

        for category, books in catalog.items():
            self.stdout.write(f'\n📂 {category}:')
            
            for title, author, description in books:
                current += 1
                isbn = f'978{random.randint(1000000000, 9999999999)}'
                page_count = random.randint(180, 550)
                year = random.randint(1950, 2024)
                month = random.randint(1, 12)
                day = random.randint(1, 28)

                book, created = Book.objects.get_or_create(
                    title=title,
                    author=author,
                    defaults={
                        'isbn': isbn,
                        'description': description,
                        'page_count': page_count,
                        'genre': category,
                        'published_date': date(year, month, day),
                        'is_available': True,
                    }
                )

                status = '✓ Added' if created else '• Exists'
                self.stdout.write(f'   {status}: {title}')
                
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Catalog populated! {created_count} new books added ({total_books} total in catalog).'
        ))
