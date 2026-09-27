class library:
    def __init__(self):
        self.users = []
        self.books = []

    def add_user(self, user):
        self.users.append(user)
        
    def add_book(self, book):
        self.books.append(book)

    def show_books(self):
        for book in self.books:
            print(book.show_book_info())

    def borrow_book(self, user, book):
        if book in self.books:
            if book.avalable:
                book.avalable = False
                print(f"Éxito: El libro '{book.title}' ha sido prestado a {user.name}.")
            else:
                print(f"Error: El libro '{book.title}' ya se encuentra prestado.")
        else:
            print("Error: El libro no pertenece a esta biblioteca.")

    def return_book(self, book):
        if book in self.books:
            if not book.avalable:
                book.avalable = True
                print(f"Éxito: El libro '{book.title}' ha sido devuelto.")
            else:
                print(f"Aviso: El libro '{book.title}' ya estaba disponible.")
        else:
            print("Error: El libro no pertenece a esta biblioteca.")