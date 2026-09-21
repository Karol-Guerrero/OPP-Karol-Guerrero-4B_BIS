# Student: Guerrero Quintero Karol Emmanuel 
# Object-Oriented Programming 4°B BIS 

class User: 
    def __init__(self, username: str, email: str, bio: str, password: str): 
        self.__username = username 
        self.__email = email 
        self.__bio = bio 
        self.__password = password

    def login(self): 
        print(f"The user @{self.__username} is logged in.")

    def create_post(self, title: str, content: str):
        print(f"@{self.__username} created a new post: {title}")


class Post: 
    def __init__(self, post_id: int, image_url: str, caption: str): 
        self.__post_id = post_id 
        self.__image_url = image_url
        self.__caption = caption 
        self.__likes_count = 0

    def like(self): 
        self.__likes_count += 1
        print(f"Post {self.__post_id} liked! Total likes: {self.__likes_count}")

    def display_post(self): 
        print(f"Post [{self.__post_id}] '{self.__caption}'(Image: {self.__image_url})")


class Comment: 
    def __init__(self, comment_id: int, author: str, text: str, receiver: str): 
        self.__comment_id = comment_id 
        self.__author = author 
        self.__text = text
        self.__receiver = receiver

    def edit_comment(self, new_text: str): 
        self.__text = new_text 
        print(f"Comment {self.__comment_id} modified.")

    def display_comment(self): 
        print(f"@{self.__author} commented to @{self.__receiver}: '{self.__text}'")


class MessageDM: 
    def __init__(self, sender: str, receiver: str, content: str): 
        self.__sender = sender
        self.__receiver = receiver
        self.__content = content
        self.__is_read = False 

    def send_message(self): 
        print(f"The message has been sent from @{self.__sender} to @{self.__receiver}: '{self.__content}'")


user1 = User("Adrian", "adrian@utd.edu.mx", "19", "pass123")
user2 = User("Dulce", "dulce@utd.edu.mx", "20", "pass123")

user1.login()
user1.create_post("Una foto con mi perrito", "Un día genial en la UTD")

post1 = Post(1, "https://foto.com/image.jpg", "Una foto con mi perrito")
post1.display_post()
post1.like()

comment1 = Comment(101, "Dulce", "¡Buena foto!", "Adrian")
comment1.display_comment()
comment1.edit_comment("¡Excelente foto!")
comment1.display_comment()

dm1 = MessageDM("Adrian", "Dulce", "Hola Adrian, ¿cómo estás?")
dm1.send_message()