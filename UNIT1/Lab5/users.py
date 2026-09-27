class user: 
    def __init__(self, id_user, name, password):
        self.id_user = id_user
        self.name = name
        self.__password = password
        

    def show_user_info(self):
        return f"{self.id_user} - {self.name}"

    