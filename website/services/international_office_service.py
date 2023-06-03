from .singleton import Singleton
from website import db
import pandas as pd
import io

class InternationalOfficeService(metaclass=Singleton):
    
    def __init__(self, user_table, university_table, applications_table, university_departments_table):
        self.user_table = user_table
        self.university_table = university_table
        self.applications_table = applications_table
        self.university_departments_table = university_departments_table

    def getAppliedStudents(self, department:str):
        df = pd.DataFrame(columns=['FirstName', 'LastName', 'StudentID', 'Faculty', 'Department', 
                                    'Degree', 'CGPA', 'Score'])
        applications = self.applications_table.query.all()
        for application in applications:
            student_id = application.student_id
            student = self.user_table.query.filter_by(bilkent_id = student_id).first()
            if student.department == department:
                name = student.name
                name_list = name.split()
                first_name = ' '.join(name_list[:-1])
                last_name = name_list[-1]
                new_row = {'FirstName': first_name, 'LastName': last_name, 'StudentID': student_id, 
                            'Faculty': 'Faculty of Engineering', 'Department': student.department, 
                            'Degree': 'undergraduate', 'CGPA': application.cgpa, 'Score':""}
                df = df.append(new_row, ignore_index = True)

        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Applications', index=False)
        writer.save()
        output.seek(0)
        return output

    def place(self, department:str, file): # columns: StudentID | Score
        df = pd.read_excel(file)  
        sorted_df = df.sort_values(by=['Score'], ascending=False)
        rank = 1
        for index, row in sorted_df.iterrows():
            process_end = False
            application = self.applications_table.query.filter_by(student_id=row["StudentID"]).first()
            application.ranking = rank
            rank = rank + 1
            student = self.user_table.query.filter_by(bilkent_id=row["StudentID"]).first()

            university_list = []
            university1 = self.university_table.query.filter_by(name = application.selected_university_1).first()
            university2 = self.university_table.query.filter_by(name = application.selected_university_2).first()
            university3 = self.university_table.query.filter_by(name = application.selected_university_3).first()
            university4 = self.university_table.query.filter_by(name = application.selected_university_4).first()
            university5 = self.university_table.query.filter_by(name = application.selected_university_5).first()
            university_list.append(university1)
            university_list.append(university2)
            university_list.append(university3)
            university_list.append(university4)
            university_list.append(university5)

            for university in university_list:
                if university != None and process_end == False:
                    departments = university.departments 
                    for department in departments:
                        if department.department == student.department:
                            if department.remaining_quota > 0:
                                application.matched_university = university.university_id
                                department.remaining_quota = department.remaining_quota - 1
                                application.application_status = "placed"
                                process_end = True
                else:
                    if (process_end == False):
                        application.application_status = "waiting bin"
                    process_end = True
        db.session.commit() 

    def getDepartments(self):
        departments = []
        users = self.user_table.query.all()
        for user in users:
            if ((user.department in departments) == False):
                departments.append(user.department)
        return departments


    

        
        
        
        
        
        
        
        
        
        
        
        
        
        