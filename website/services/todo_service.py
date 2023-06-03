from .singleton import Singleton
from website import db
class TodoService(metaclass=Singleton):
    def __init__(self, user_table, todo_table):
        self.user_table = user_table
        self.todo_table = todo_table
    
    def deleteTask(self, task_id: int):
        task = self.todo_table.query.filter_by(task_id = task_id).first()
        print(task_id)
        db.session.delete(task)
        db.session.commit()

    def postTask(self, bilkent_id : int, task : str):
        if len(task) > 0:
            task = self.todo_table(task = task, user_id = bilkent_id)
            db.session.add(task)
            db.session.commit()
        
      