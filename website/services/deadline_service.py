from .singleton import Singleton

from datetime import datetime
from website import db

class DeadlineService(metaclass=Singleton):
    def __init__(self, deadlines_table):
        self.deadlines_table = deadlines_table
    
    def get_deadline(self, deadline_title: str):
        """ 
            You can compare the datetime objects using comparison operators (=, <, >, <=, >=) 
        """
    
        deadline = self.deadlines_table.query.filter_by(deadline_title=deadline_title).first()
        deadline_str = deadline.deadline
        
        deadline_obj = datetime.strptime(deadline_str, "%d/%m/%y %H.%M")
        
        return deadline_obj
    
    def get_todays_date(self):
        todays_date = datetime.now()
        return todays_date
    
    def has_passed(self, deadline_title: str):
        """
            If has passed is True, it means the deadline has passed 
        """
        
        deadline = self.get_deadline(deadline_title)
        todays_date = self.get_todays_date()
        
        return todays_date > deadline
        
    def get_all_deadlines(self):
        return self.deadlines_table.query.all()

    def get_all_deadlines_format_calendar(self):
        deadlines = self.get_all_deadlines()
        # list is preferred as order matters, map oobject lacks the required sequence
        deadline_list = ["now", datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M")]
        for deadline in deadlines:
            deadline_t = datetime.strptime(deadline.deadline, "%d/%m/%y %H.%M")
            deadline_s = datetime.strftime(deadline_t, "%Y-%m-%dT%H:%M")
            if (datetime.now() < deadline_t):
                deadline_list.append(deadline.deadline_title.replace("_", " ").rsplit(" ", 1)[0] + " period")
                deadline_list.append(deadline_s)
        return deadline_list
    
    def update_deadline(self, deadline_title: str, deadline_str: str):
        if (deadline_title != "application_deadline" 
                and deadline_title != "preapproval_deadline" 
                and deadline_title != "learning_agreement_deadline"):
            return None

        deadline = self.deadlines_table.query.filter_by(deadline_title=deadline_title).first()
        deadline.deadline = deadline_str
        db.session.commit()
        return deadline
        