#Exersice 1
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def introduce(self):
        print(f"Hi, my name is {self.name}")


class Post:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def show_post(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author.name}")
        print(f"Content: {self.content}")


user1 = User("Carlos", "carlos@email.com")

post1 = Post(
    "My first post",
    "I am learning Python!",
    user1
)

post1.show_post()

#Exercise 2
class User:
    def __init__(self, name):
        name = name


user1 = User("Carlos")

print(user1.name)

#Exercise 3
class Post:
    def __init__(self, title, author):
        self.title = title
        self.author = author


user1 = User("Carlos")

post1 = Post("Hello!", "Carlos")

#Exercise 4
class User:
    def __init__(self, name):
        self.name = name


class Post:
    def __init__(self, title, author):
        self.title = title
        self.author = author


user1 = User("Carlos")
post1 = Post("My First Post", user1)

print(post1.author.name)