# data_management.py
import os
import django
import pandas as pd
import numpy as np
from datetime import datetime
import random
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from books.models import Author, Genre, Book

class DataManager:
    def __init__(self):
        self.imported_authors = 0
        self.imported_genres = 0
        self.imported_books = 0
        
    def clean_author_data(self, df):
        """Clean and validate author data"""
        print("Cleaning author data...")
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['AuthorID'], keep='first')
        
        # Handle missing values
        df['FirstName'] = df['FirstName'].fillna('Unknown')
        df['LastName'] = df['LastName'].fillna('Author')
        df['Bio'] = df['Bio'].fillna('No biography available.')
        df['Image'] = df['Image'].fillna('')
        
        # Clean string fields
        df['FirstName'] = df['FirstName'].str.strip()
        df['LastName'] = df['LastName'].str.strip()
        df['Bio'] = df['Bio'].str.strip()
        
        # Validate date formats
        df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'], errors='coerce')
        df['DateOfDeath'] = pd.to_datetime(df['DateOfDeath'], errors='coerce')
        
        # Ensure AuthorID is integer
        df['AuthorID'] = df['AuthorID'].astype(int)
        
        print(f"Cleaned {len(df)} author records")
        return df
    
    def clean_genre_data(self, df):
        """Clean and validate genre data"""
        print("Cleaning genre data...")
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['GenreID'], keep='first')
        df = df.drop_duplicates(subset=['GenreName'], keep='first')
        
        # Handle missing values and clean
        df['GenreName'] = df['GenreName'].fillna('Unknown Genre')
        df['GenreName'] = df['GenreName'].str.strip().str.title()
        
        # Ensure GenreID is integer
        df['GenreID'] = df['GenreID'].astype(int)
        
        print(f"Cleaned {len(df)} genre records")
        return df
    
    def clean_book_data(self, df):
        """Clean and validate book data"""
        print("Cleaning book data...")
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['ISBN'], keep='first')
        df = df.drop_duplicates(subset=['Title'], keep='first')
        
        # Handle missing values
        df['Title'] = df['Title'].fillna('Unknown Title')
        df['Publisher'] = df['Publisher'].fillna('Unknown Publisher')
        df['Photo'] = df['Photo'].fillna('')
        
        # Clean string fields
        df['Title'] = df['Title'].str.strip()
        df['ISBN'] = df['ISBN'].astype(str).str.strip()
        df['Publisher'] = df['Publisher'].str.strip()
        
        # Handle prices - generate random if missing
        df['Price'] = df['Price'].apply(self.clean_price)
        
        # Handle stock - generate random if missing
        df['Stock'] = df['Stock'].apply(lambda x: x if pd.notna(x) and x >= 0 else random.randint(0, 20))
        
        # Handle publication dates
        df['PublicationDate'] = df.apply(
            lambda row: self.create_publication_date(
                row.get('Publish Date (Month)', None),
                row.get('Publish Date (Year)', None)
            ), axis=1
        )
        
        # Ensure BookID is integer
        df['BookID'] = df['BookID'].astype(int)
        
        print(f"Cleaned {len(df)} book records")
        return df
    
    def clean_price(self, price_value):
        """Clean and validate price data"""
        if pd.isna(price_value) or price_value == '':
            return round(random.uniform(9.99, 99.99), 2)
        
        try:
            price_str = str(price_value).replace('$', '').replace(',', '').strip()
            price = float(price_str)
            return max(0, round(price, 2))  # Ensure non-negative
        except (ValueError, TypeError):
            return round(random.uniform(9.99, 99.99), 2)
    
    def create_publication_date(self, month, year):
        """Create publication date from month and year"""
        if pd.isna(year) or year == '':
            return None
        
        try:
            year = int(float(year))
            month_val = int(float(month)) if pd.notna(month) and month != '' else 1
            
            # Validate month range
            if month_val < 1 or month_val > 12:
                month_val = 1
                
            return f"{year}-{month_val:02d}-01"
        except (ValueError, TypeError):
            return None
    
    def import_authors(self, csv_file):
        """Import authors from CSV to database"""
        print(f"Importing authors from {csv_file}...")
        
        try:
            df = pd.read_csv(csv_file)
            df = self.clean_author_data(df)
            
            authors_created = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Handle date fields
                    dob = None
                    if pd.notna(row['DateOfBirth']):
                        try:
                            dob = row['DateOfBirth'].date() if hasattr(row['DateOfBirth'], 'date') else datetime.strptime(str(row['DateOfBirth']), '%Y-%m-%d').date()
                        except:
                            dob = None
                    
                    dod = None
                    if pd.notna(row['DateOfDeath']):
                        try:
                            dod = row['DateOfDeath'].date() if hasattr(row['DateOfDeath'], 'date') else datetime.strptime(str(row['DateOfDeath']), '%Y-%m-%d').date()
                        except:
                            dod = None
                    
                    # Create or update author
                    author, created = Author.objects.update_or_create(
                        AuthorID=row['AuthorID'],
                        defaults={
                            'FirstName': row['FirstName'][:100],
                            'LastName': row['LastName'][:100],
                            'Bio': row['Bio'] or '',
                            'DateOfBirth': dob,
                            'DateOfDeath': dod,
                            'Image': row['Image'][:200] if pd.notna(row['Image']) else ''
                        }
                    )
                    
                    if created:
                        authors_created += 1
                        
                except Exception as e:
                    errors.append(f"AuthorID {row['AuthorID']}: {str(e)}")
            
            self.imported_authors = authors_created
            print(f"✓ Successfully imported {authors_created} authors")
            
            if errors:
                print(f"⚠️  {len(errors)} errors occurred:")
                for error in errors[:5]:
                    print(f"   - {error}")
                if len(errors) > 5:
                    print(f"   ... and {len(errors) - 5} more errors")
                    
            return authors_created
            
        except Exception as e:
            print(f"❌ Error importing authors: {e}")
            return 0
    
    def import_genres(self, csv_file):
        """Import genres from CSV to database"""
        print(f"Importing genres from {csv_file}...")
        
        try:
            df = pd.read_csv(csv_file)
            df = self.clean_genre_data(df)
            
            genres_created = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    genre, created = Genre.objects.update_or_create(
                        GenreID=row['GenreID'],
                        defaults={
                            'GenreName': row['GenreName'][:100]
                        }
                    )
                    
                    if created:
                        genres_created += 1
                        
                except Exception as e:
                    errors.append(f"GenreID {row['GenreID']}: {str(e)}")
            
            self.imported_genres = genres_created
            print(f"✓ Successfully imported {genres_created} genres")
            
            if errors:
                print(f"⚠️  {len(errors)} errors occurred:")
                for error in errors[:5]:
                    print(f"   - {error}")
                    
            return genres_created
            
        except Exception as e:
            print(f"❌ Error importing genres: {e}")
            return 0
    
    def import_books(self, csv_file):
        """Import books from CSV to database"""
        print(f"Importing books from {csv_file}...")
        
        try:
            df = pd.read_csv(csv_file)
            df = self.clean_book_data(df)
            
            books_created = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Get author and genre
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
                    
                    # Handle publication date
                    pub_date = None
                    if pd.notna(row['PublicationDate']):
                        try:
                            pub_date = datetime.strptime(str(row['PublicationDate']), '%Y-%m-%d').date()
                        except:
                            pub_date = None
                    
                    # Create or update book
                    book, created = Book.objects.update_or_create(
                        BookID=row['BookID'],
                        defaults={
                            'Title': row['Title'][:200],
                            'AuthorID': author,
                            'GenreID': genre,
                            'ISBN': str(row['ISBN'])[:13],
                            'Publisher': row['Publisher'][:200],
                            'PublicationDate': pub_date,
                            'Price': Decimal(str(row['Price'])),
                            'Stock': int(row['Stock']),
                            'Photo': row['Photo'][:200] if pd.notna(row['Photo']) else ''
                        }
                    )
                    
                    if created:
                        books_created += 1
                        
                except Exception as e:
                    errors.append(f"BookID {row['BookID']}: {str(e)}")
            
            self.imported_books = books_created
            print(f"✓ Successfully imported {books_created} books")
            
            if errors:
                print(f"⚠️  {len(errors)} errors occurred:")
                for error in errors[:5]:
                    print(f"   - {error}")
                if len(errors) > 5:
                    print(f"   ... and {len(errors) - 5} more errors")
                    
            return books_created
            
        except Exception as e:
            print(f"❌ Error importing books: {e}")
            return 0
    
    def export_data(self, export_dir='exports'):
        """Export current database data to CSV files"""
        print(f"Exporting data to {export_dir}...")
        
        # Create export directory
        os.makedirs(export_dir, exist_ok=True)
        
        # Export authors
        authors_data = []
        for author in Author.objects.all():
            authors_data.append({
                'AuthorID': author.AuthorID,
                'FirstName': author.FirstName,
                'LastName': author.LastName,
                'Bio': author.Bio,
                'DateOfBirth': author.DateOfBirth,
                'DateOfDeath': author.DateOfDeath,
                'Image': author.Image
            })
        
        authors_df = pd.DataFrame(authors_data)
        authors_df.to_csv(f'{export_dir}/authors_export.csv', index=False)
        print(f"✓ Exported {len(authors_df)} authors to {export_dir}/authors_export.csv")
        
        # Export genres
        genres_data = []
        for genre in Genre.objects.all():
            genres_data.append({
                'GenreID': genre.GenreID,
                'GenreName': genre.GenreName
            })
        
        genres_df = pd.DataFrame(genres_data)
        genres_df.to_csv(f'{export_dir}/genres_export.csv', index=False)
        print(f"✓ Exported {len(genres_df)} genres to {export_dir}/genres_export.csv")
        
        # Export books
        books_data = []
        for book in Book.objects.all():
            books_data.append({
                'BookID': book.BookID,
                'Title': book.Title,
                'AuthorID': book.AuthorID.AuthorID,
                'GenreID': book.GenreID.GenreID,
                'ISBN': book.ISBN,
                'Publisher': book.Publisher,
                'PublicationDate': book.PublicationDate,
                'Price': float(book.Price),
                'Stock': book.Stock,
                'Photo': book.Photo
            })
        
        books_df = pd.DataFrame(books_data)
        books_df.to_csv(f'{export_dir}/books_export.csv', index=False)
        print(f"✓ Exported {len(books_df)} books to {export_dir}/books_export.csv")
        
        return len(authors_df), len(genres_df), len(books_df)
    
    def generate_sample_data(self):
        """Generate sample data if no CSV files exist"""
        print("Generating sample data...")
        
        # Sample genres
        sample_genres = [
            'Fiction', 'Science Fiction', 'Mystery', 'Romance', 'Thriller',
            'Biography', 'History', 'Science', 'Fantasy', 'Horror',
            'Young Adult', 'Children', 'Cookbook', 'Travel', 'Art',
            'Philosophy', 'Psychology', 'Business', 'Technology', 'Health'
        ]
        
        for i, genre_name in enumerate(sample_genres, 1):
            Genre.objects.get_or_create(
                GenreID=i,
                defaults={'GenreName': genre_name}
            )
        
        # Sample authors
        sample_authors = [
            {'FirstName': 'George', 'LastName': 'Orwell', 'Bio': 'English novelist and essayist.'},
            {'FirstName': 'Jane', 'LastName': 'Austen', 'Bio': 'English novelist known for social commentary.'},
            {'FirstName': 'Stephen', 'LastName': 'King', 'Bio': 'American author of horror and fantasy novels.'},
            # Add more sample authors as needed
        ]
        
        for i, author_data in enumerate(sample_authors, 1):
            Author.objects.get_or_create(
                AuthorID=i,
                defaults=author_data
            )
        
        print("✓ Sample data generated")
    
    def validate_data(self):
        """Validate imported data"""
        print("\n=== DATA VALIDATION ===")
        
        author_count = Author.objects.count()
        genre_count = Genre.objects.count()
        book_count = Book.objects.count()
        
        print(f"Authors in database: {author_count}")
        print(f"Genres in database: {genre_count}")
        print(f"Books in database: {book_count}")
        
        # Check for books with invalid foreign keys
        invalid_author_books = Book.objects.filter(AuthorID__isnull=True).count()
        invalid_genre_books = Book.objects.filter(GenreID__isnull=True).count()
        
        if invalid_author_books > 0:
            print(f"⚠️  Warning: {invalid_author_books} books have invalid AuthorID")
        
        if invalid_genre_books > 0:
            print(f"⚠️  Warning: {invalid_genre_books} books have invalid GenreID")
        
        # Check for negative prices or stock
        negative_price_books = Book.objects.filter(Price__lt=0).count()
        negative_stock_books = Book.objects.filter(Stock__lt=0).count()
        
        if negative_price_books > 0:
            print(f"⚠️  Warning: {negative_price_books} books have negative prices")
        
        if negative_stock_books > 0:
            print(f"⚠️  Warning: {negative_stock_books} books have negative stock")
        
        return author_count, genre_count, book_count

def main():
    """Main function to run the data management process"""
    manager = DataManager()
    
    print("=== DJANGO DATA MANAGEMENT TOOL ===")
    print("This tool will:")
    print("1. Clean and format your data")
    print("2. Import data from CSV files")
    print("3. Export data to CSV files")
    print("4. Validate the imported data")
    print()
    
    # File paths
    authors_file = 'authors_transformed.csv'
    genres_file = 'genres_transformed.csv'
    books_file = 'books.csv'
    
    # Check if CSV files exist, otherwise generate sample data
    if not all(os.path.exists(f) for f in [authors_file, genres_file, books_file]):
        print("CSV files not found. Generating sample data...")
        manager.generate_sample_data()
    else:
        # Import data
        authors_imported = manager.import_authors(authors_file)
        genres_imported = manager.import_genres(genres_file)
        books_imported = manager.import_books(books_file)
        
        print(f"\n=== IMPORT SUMMARY ===")
        print(f"Authors imported: {authors_imported}")
        print(f"Genres imported: {genres_imported}")
        print(f"Books imported: {books_imported}")
    
    # Validate data
    author_count, genre_count, book_count = manager.validate_data()
    
    # Export data (for verification)
    print(f"\n=== EXPORTING DATA ===")
    exported_authors, exported_genres, exported_books = manager.export_data()
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"✅ Data management completed successfully!")
    print(f"📊 Database contains:")
    print(f"   - {author_count} authors")
    print(f"   - {genre_count} genres") 
    print(f"   - {book_count} books")
    print(f"💾 Data exported to 'exports/' directory")
    print(f"🔍 You can now check the data in Django admin panel")

if __name__ == "__main__":
    main()