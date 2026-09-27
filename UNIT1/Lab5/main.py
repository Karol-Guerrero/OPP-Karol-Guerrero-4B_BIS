from books import book
from users import user
from library import library

book1 = book("001", "OPP Fundamentals", "Jhon L", "BBC")
book2 = book("002", "Python For Dummies", "Stef Maruzh", "For Dummies")

user1 = user("001", "Guerrero Karol", "1234")  
library = library()
library.add_book(book1)
library.add_book(book2)
library.add_user(user1)
library.show_books()

#Requeriments 
#1. The system must allow registrer books. 
#2. The system must allow registrer users.
#3. The system must allow a book to be borrowed by a user.
#4. A book that has already been borrowed must not be borrowed again.
#5. The system must allow a book to be returned.

print("\n--- Demostración de Préstamos y Devoluciones ---")
library.borrow_book(user1, book1)
library.borrow_book(user1, book1)
library.return_book(book1)
library.borrow_book(user1, book1)