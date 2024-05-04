class Book:
    def __init__(self, title, author, genre, isbn, available=True):
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn
        self.available = available

    def to_string(self):
        return f"{self.title},{self.author},{self.genre},{self.isbn},{self.available}\n"

class Library:
    def __init__(self, input_file_path, output_file_path):
        self.books = []
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.load_books_from_file()

    def load_books_from_file(self):
        try:
            with open(self.input_file_path, 'r') as file:
                for line in file:
                    title, author, genre, isbn, available = line.strip().split(',')
                    self.books.append(Book(title, author, genre, isbn, available=="True"))
        except Exception as e:
            print(f"An error occurred while loading the library file: {e}")
            print("Starting with an empty library.")

    def save_books_to_file(self):
        with open(self.output_file_path, 'w') as file:
            for book in self.books:
                file.write(book.to_string())

    def add_book(self, book):
        self.books.append(book)
        self.save_books_to_file()
        print(f"{book.title} has been added to the library inventory")

    def remove_book(self, book_title):
        for book in self.books:
            if book.title == book_title:
                self.books.remove(book)
                self.save_books_to_file()
                print(f"{book.title} has been removed from the library inventory")
                return
        print("Book not found in the library inventory")

    def display_all_books(self):
        print("Books in the library inventory:")
        for book in self.books:
            print(f"{book.title} by {book.author} - {book.genre}")

    def search_book(self, keyword):
        found_books = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower() or keyword.lower() == book.isbn.lower():
                found_books.append(book)
        if found_books:
            print("Search results:")
            for book in found_books:
                print(f"{book.title} by {book.author}")
        else:
            print("No matching books found")

    def lend_book(self, book_title, user):
        for book in self.books:
            if book.title == book_title and book.available:
                book.available = False
                self.save_books_to_file()
                user.books_borrowed.append(book)
                print(f"{book.title} has been borrowed by {user.name}")
                return
        print("Book not available")

    def return_book(self, book_title, user):
        for book in user.books_borrowed:
            if book.title == book_title:
                book.available = True
                self.save_books_to_file()
                user.books_borrowed.remove(book)
                print(f"{book.title} has been returned by {user.name}")
                return
        print("Book not borrowed by this user")

    def display_books_borrowed_by_user(self, user):
        if user.books_borrowed:
            print(f"Books borrowed by {user.name}:")
            for book in user.books_borrowed:
                print(f"{book.title} by {book.author}")
        else:
            print(f"{user.name} has not borrowed any books")

    def sort_books_by_genre(self, genre):
        genre_books = [book for book in self.books if book.genre.lower() == genre.lower()]
        if genre_books:
            print(f"Books in the {genre} genre:")
            for book in genre_books:
                print(f"{book.title} by {book.author}")
        else:
            print(f"No books found in the {genre} genre")

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.books_borrowed = []

# Example usage
library = Library("Knygos", "Knygos1")

# Add, remove, and perform other operations on the library...

library.display_all_books()
library.sort_books_by_genre("Fantasy")
