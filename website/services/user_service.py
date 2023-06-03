from .singleton import Singleton
from website.models import User
from website import db

class UserService(metaclass=Singleton):
    def __init__(self, user_table):
        self.user_table = user_table
        
    def getUserById(self, id: int):
        user: User = self.user_table.query.filter_by(bilkent_id = id).first()
        return user

    def getAllUsers(self):
        contacts_list = self.user_table.query.all()
        return contacts_list
    
