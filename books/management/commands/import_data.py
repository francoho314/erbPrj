# books/management/commands/import_data.py
import pandas as pd
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from books.models import Author, Genre, Book  

class Command(BaseCommand):
    help = 'Import data from CSV files to database tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--authors',
            type=str,
            default='authors_transformed.csv',
            help='Path to authors CSV file',
        )
        parser.add_argument(
            '--genres', 
            type=str,
            default='genres_transformed.csv',
            help='Path to genres CSV file',
        )
        parser.add_argument(
            '--books',
            type=str,
            default='books.csv',
            help='Path to books CSV file',
        )
        parser.add_argument(
            '--reset-sequences',
            action='store_true',
            help='Reset database sequences after import',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data import process...'))
        
        authors_file = options['authors']
        genres_file = options['genres']
        books_file = options['books']
        
        try:
            # Import in correct order to maintain foreign key relationships
            # 1. Import Authors first
            if self.file_exists(authors_file):
                author_count = self.import_authors(authors_file)
            else:
                self.stderr.write(f"Error: Authors file not found: {authors_file}")
                return

            # 2. Import Genres second
            if self.file_exists(genres_file):
                genre_count = self.import_genres(genres_file)
            else:
                self.stderr.write(f"Error: Genres file not found: {genres_file}")
                return

            # 3. Import Books last (depends on Authors and Genres)
            if self.file_exists(books_file):
                book_count = self.import_books(books_file)
            else:
                self.stderr.write(f"Error: Books file not found: {books_file}")
                return

            # Reset sequences if requested
            if options['reset_sequences']:
                self.reset_sequences()

            # Validate imported data
            self.validate_data()

            self.stdout.write(
                self.style.SUCCESS(f"\n=== IMPORT SUMMARY ===")
            )
            self.stdout.write(f"Authors processed: {author_count}")
            self.stdout.write(f"Genres processed: {genre_count}")
            self.stdout.write(f"Books processed: {book_count}")
            self.stdout.write(self.style.SUCCESS("Data import completed successfully!"))

        except Exception as e:
            self.stderr.write(f"Error during import process: {str(e)}")
            import traceback
            traceback.print_exc()

    def file_exists(self, file_path):
        """Check if file exists"""
        import os
        return os.path.exists(file_path)

    def import_authors(self, csv_file):
        """Import authors from CSV to Author model"""
        self.stdout.write(f"Importing authors from {csv_file}...")
        
        df = pd.read_csv(csv_file)
        authors_created = 0
        authors_updated = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Handle date fields
                dob = None
                if pd.notna(row['DateOfBirth']):
                    try:
                        dob = datetime.strptime(str(row['DateOfBirth']), '%Y-%m-%d').date()
                    except ValueError:
                        dob = None
                
                dod = None
                if pd.notna(row['DateOfDeath']):
                    try:
                        dod = datetime.strptime(str(row['DateOfDeath']), '%Y-%m-%d').date()
                    except ValueError:
                        dod = None
                
                # Handle empty strings for Bio and Image
                bio = row['Bio'] if pd.notna(row['Bio']) and str(row['Bio']).strip() != '' else ''
                image = row['Image'] if pd.notna(row['Image']) and str(row['Image']).strip() != '' else ''
                
                # Use update_or_create to handle existing records
                author, created = Author.objects.update_or_create(
                    AuthorID=row['AuthorID'],
                    defaults={
                        'FirstName': row['FirstName'][:100],  # Truncate to max_length
                        'LastName': row['LastName'][:100],    # Truncate to max_length
                        'Bio': bio,
                        'DateOfBirth': dob,
                        'DateOfDeath': dod,
                        'Image': image[:200]  # Truncate to max_length
                    }
                )
                
                if created:
                    authors_created += 1
                else:
                    authors_updated += 1
                    
            except Exception as e:
                errors.append(f"AuthorID {row['AuthorID']}: {str(e)}")
        
        self.stdout.write(f"Authors import completed:")
        self.stdout.write(f"  Authors created: {authors_created}")
        self.stdout.write(f"  Authors updated: {authors_updated}")
        self.stdout.write(f"  Errors: {len(errors)}")
        
        if errors:
            self.stderr.write("\nErrors encountered:")
            for error in errors[:10]:
                self.stderr.write(f"  - {error}")
            if len(errors) > 10:
                self.stderr.write(f"  ... and {len(errors) - 10} more errors")
        
        return authors_created + authors_updated

    def import_genres(self, csv_file):
        """Import genres from CSV to Genre model"""
        self.stdout.write(f"Importing genres from {csv_file}...")
        
        df = pd.read_csv(csv_file)
        genres_created = 0
        genres_updated = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Use update_or_create to handle existing records
                genre, created = Genre.objects.update_or_create(
                    GenreID=row['GenreID'],
                    defaults={
                        'GenreName': row['GenreName'][:100]  # Truncate to max_length
                    }
                )
                
                if created:
                    genres_created += 1
                else:
                    genres_updated += 1
                    
            except Exception as e:
                errors.append(f"GenreID {row['GenreID']}: {str(e)}")
        
        self.stdout.write(f"Genres import completed:")
        self.stdout.write(f"  Genres created: {genres_created}")
        self.stdout.write(f"  Genres updated: {genres_updated}")
        self.stdout.write(f"  Errors: {len(errors)}")
        
        if errors:
            self.stderr.write("\nErrors encountered:")
            for error in errors[:10]:
                self.stderr.write(f"  - {error}")
            if len(errors) > 10:
                self.stderr.write(f"  ... and {len(errors) - 10} more errors")
        
        return genres_created + genres_updated

    def import_books(self, csv_file):
        """Import books from CSV to Book model"""
        self.stdout.write(f"Importing books from {csv_file}...")
        
        df = pd.read_csv(csv_file)
        books_created = 0
        books_updated = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Handle publication date
                pub_date = None
                if pd.notna(row['PublicationDate']):
                    try:
                        pub_date = datetime.strptime(str(row['PublicationDate']), '%Y-%m-%d').date()
                    except ValueError:
                        pub_date = None
                
                # Get Author and Genre instances
                try:
                    author = Author.objects.get(AuthorID=row['AuthorID'])
                except Author.DoesNotExist:
                    errors.append(f"BookID {row['BookID']}: AuthorID {row['AuthorID']} not found")
                    continue
                    
                try:
                    genre = Genre.objects.get(GenreID=row['GenreID'])
                except Genre.DoesNotExist:
                    errors.append(f"BookID {row['BookID']}: GenreID {row['GenreID']} not found")
                    continue
                
                # Handle empty strings
                publisher = row['Publisher'] if pd.notna(row['Publisher']) and str(row['Publisher']).strip() != '' else ''
                photo = row['Photo'] if pd.notna(row['Photo']) and str(row['Photo']).strip() != '' else ''
                
                # Ensure price is not negative
                price = Decimal(str(row['Price']))
                if price < 0:
                    price = Decimal('0.00')
                
                # Ensure stock is not negative
                stock = int(row['Stock'])
                if stock < 0:
                    stock = 0
                
                # Use update_or_create to handle existing records
                book, created = Book.objects.update_or_create(
                    BookID=row['BookID'],
                    defaults={
                        'Title': row['Title'][:200],  # Truncate to max_length
                        'AuthorID': author,
                        'GenreID': genre,
                        'ISBN': str(row['ISBN'])[:13],  # Truncate to max_length
                        'Publisher': publisher[:200],    # Truncate to max_length
                        'PublicationDate': pub_date,
                        'Price': price,
                        'Stock': stock,
                        'Photo': photo[:200]  # Truncate to max_length
                    }
                )
                
                if created:
                    books_created += 1
                else:
                    books_updated += 1
                    
            except Exception as e:
                errors.append(f"BookID {row['BookID']}: {str(e)}")
        
        self.stdout.write(f"Books import completed:")
        self.stdout.write(f"  Books created: {books_created}")
        self.stdout.write(f"  Books updated: {books_updated}")
        self.stdout.write(f"  Errors: {len(errors)}")
        
        if errors:
            self.stderr.write("\nErrors encountered:")
            for error in errors[:10]:
                self.stderr.write(f"  - {error}")
            if len(errors) > 10:
                self.stderr.write(f"  ... and {len(errors) - 10} more errors")
        
        return books_created + books_updated

    def reset_sequences(self):
        """Reset database sequences after manual ID insertion"""
        from django.db import connection
        
        self.stdout.write("Resetting database sequences...")
        
        with connection.cursor() as cursor:
            # For PostgreSQL
            try:
                # Replace 'books' with your actual app name
                cursor.execute("SELECT setval('books_author_authorid_seq', (SELECT MAX(AuthorID) FROM books_author))")
                cursor.execute("SELECT setval('books_genre_genreid_seq', (SELECT MAX(GenreID) FROM books_genre))")
                cursor.execute("SELECT setval('books_book_bookid_seq', (SELECT MAX(BookID) FROM books_book))")
                self.stdout.write("Sequences reset successfully for PostgreSQL")
            except Exception as e:
                # For SQLite, sequences are handled automatically
                self.stdout.write(f"Sequences reset not required or not supported: {e}")
                pass

    def validate_data(self):
        """Validate that all data was imported correctly"""
        self.stdout.write("\n=== DATA VALIDATION ===")
        
        author_count = Author.objects.count()
        genre_count = Genre.objects.count()
        book_count = Book.objects.count()
        
        self.stdout.write(f"Authors in database: {author_count}")
        self.stdout.write(f"Genres in database: {genre_count}")
        self.stdout.write(f"Books in database: {book_count}")
        
        # Check for books with invalid foreign keys
        invalid_author_books = Book.objects.filter(AuthorID__isnull=True).count()
        invalid_genre_books = Book.objects.filter(GenreID__isnull=True).count()
        
        if invalid_author_books > 0:
            self.stderr.write(f"Warning: {invalid_author_books} books have invalid AuthorID")
        
        if invalid_genre_books > 0:
            self.stderr.write(f"Warning: {invalid_genre_books} books have invalid GenreID")
        
        # Check for negative prices or stock
        negative_price_books = Book.objects.filter(Price__lt=0).count()
        negative_stock_books = Book.objects.filter(Stock__lt=0).count()
        
        if negative_price_books > 0:
            self.stderr.write(f"Warning: {negative_price_books} books have negative prices")
        
        if negative_stock_books > 0:
            self.stderr.write(f"Warning: {negative_stock_books} books have negative stock")