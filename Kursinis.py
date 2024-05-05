class Book:
    def __init__(self, title, author, genre, available=True):
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available

    def to_string(self):
        return f"{self.title},{self.author},{self.genre},{self.available}\n"


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.books_borrowed = []


class Library:
    def __init__(self, input_file_path, output_file_path, users_file_path):
        self.books = []
        self.users = []
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.users_file_path = users_file_path
        self.load_books_from_file()
        self.load_users_from_file()

    def load_books_from_file(self):
        try:
            with open(self.input_file_path, 'r') as file:
                for line in file:
                    title, author, genre, available = line.strip().split(',')
                    self.books.append(Book(title, author, genre, available == "True"))
        except Exception as e:
            print(f"An error occurred while loading the library file: {e}")
            print("Starting with an empty library.")

    def load_users_from_file(self):
        try:
            with open(self.users_file_path, 'r') as file:
                for line in file:
                    name, user_id = line.strip().split(',')
                    self.users.append(User(name, user_id))
        except FileNotFoundError:
            print("Naudotojai file not found. Starting with an empty list of users.")

    def save_books_to_file(self):
        with open(self.output_file_path, 'w') as file:
            for book in self.books:
                file.write(book.to_string())

    def save_users_to_file(self):
        with open(self.users_file_path, 'w') as file:
            for user in self.users:
                file.write(f"{user.name},{user.user_id}\n")

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
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower() or keyword.lower() in book.genre.lower():
                found_books.append(book)
        if found_books:
            print("Search results:")
            for book in found_books:
                print(f"{book.title} by {book.author}")
        else:
            print("No matching books found")

    def lend_book(self, book_title, user_id):
        for book in self.books:
            if book.title == book_title and book.available:
                book.available = False
                user = self.get_user_by_id(user_id)
                if user:
                    user.books_borrowed.append(book)
                    self.save_books_to_file()
                    print(f"{book.title} has been borrowed by {user.name}")
                    return
                else:
                    print("User not found.")
                    return
        print("Book not available")

    def return_book(self, book_title, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            for book in user.books_borrowed:
                if book.title == book_title:
                    book.available = True
                    user.books_borrowed.remove(book)
                    self.save_books_to_file()
                    print(f"{book.title} has been returned by {user.name}")
                    return
            print("Book not borrowed by this user")
        else:
            print("User not found.")

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def display_books_borrowed_by_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            if user.books_borrowed:
                print(f"Books borrowed by {user.name}:")
                for book in user.books_borrowed:
                    print(f"{book.title} by {book.author}")
            else:
                print(f"{user.name} has not borrowed any books")
        else:
            print("User not found.")

    def sort_books_by_genre(self, genre):
        genre_books = [book for book in self.books if book.genre.lower() == genre.lower()]
        if genre_books:
            print(f"Books in the {genre} genre:")
            for book in genre_books:
                print(f"{book.title} by {book.author}")
        else:
            print(f"No books found in the {genre} genre")

    def add_book_interface(self):
        print("Adding a new book:")
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        genre = input("Enter the genre of the book: ")
        new_book = Book(title, author, genre)
        self.add_book(new_book)

    def display_available_books(self):
        available_books = [book for book in self.books if book.available]
        if available_books:
            print("Available books in the library:")
            for idx, book in enumerate(available_books, 1):
                print(f"{idx}. {book.title} by {book.author}")
        else:
            print("No available books in the library.")

    def delete_book_interface(self):
        print("Deleting a book:")
        title = input("Enter the title of the book to delete: ")
        self.remove_book(title)

    def display_books_by_genre_interface(self):
        print("Displaying books by genre:")
        genre = input("Enter the genre to display books for: ")
        self.sort_books_by_genre(genre)


def display_menu():
    print("\nMenu:")
    print("1. Add a book")
    print("2. Display available books")
    print("3. Delete a book")
    print("4. Display books by genre")
    print("5. Lend a book")
    print("6. Return a book")
    print("7. Display books borrowed by user")
    print("8. Exit")



library = Library("Knygos.txt", "Knygos1.txt", "Naudotojai.txt")

while True:
    display_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        library.add_book_interface()
    elif choice == "2":
        library.display_available_books()
    elif choice == "3":
        library.delete_book_interface()
    elif choice == "4":
        library.display_books_by_genre_interface()
    elif choice == "5":
        book_title = input("Enter the title of the book to lend: ")
        user_id = input("Enter the user ID: ")
        library.lend_book(book_title, user_id)
    elif choice == "6":
        book_title = input("Enter the title of the book to return: ")
        user_id = input("Enter the user ID: ")
        library.return_book(book_title, user_id)
    elif choice == "7":
        user_id = input("Enter the user ID to display books borrowed: ")
        library.display_books_borrowed_by_user(user_id)
    elif choice == "8":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
