from .singleton import Singleton
from website import db

class FinalFormsService(metaclass=Singleton):   
    def __init__(self, user_table):
        self.user_table = user_table