from .singleton import Singleton

from website import db
from io import BytesIO
from .document_strategy import *
class ApplicationsService(metaclass=Singleton):
    def __init__(self, user_table, application_table, university_table, course_table):
        self.user_table = user_table
        self.application_table = application_table
        self.university_table = university_table
        self.course_table = course_table
        self.document_strategy = None
        
    def getApplicationById(self, id: int):
        task = self.application_table.query.filter_by(application_id = id).first()
        return task
    
    def getApplicationByStudentId(self, student_id: int):
        application = self.application_table.query.filter_by(student_id=student_id).first()
        if application == None:
            new_application = self.application_table(student_id=student_id, application_status="not applied")
            db.session.add(new_application)
            db.commit()
            
            application = self.application_table.query.filter_by(student_id=student_id).first()
            
        return application

    def getApplicationsByDepartment(self, dep: str):
        applications = self.application_table.query.filter_by(department = dep).all()
        return applications
    
    def getApplicationsByDepartment(self, dep: str):
        applications = self.application_table.query.all()
        
        applications_by_department = [application for application in applications if(self.user_table.query.filter_by(bilkent_id=application.student_id).first().department == dep)]
                
        return applications_by_department

    def getApplicationsByStatus(self, status: str):
        applications = self.application_table.query.filter_by(application_status=status).order_by(self.application_table.ranking).all()
        return applications
    
    def getApplicationsByStatus(self, status: str, dep: str):
        applications = self.application_table.query.filter_by(application_status=status).order_by(self.application_table.ranking).all()        
        applications_by_department = [application for application in applications if(self.user_table.query.filter_by(bilkent_id=application.student_id).first().department == dep)]  
        return applications_by_department

    def insertUniversitySelections(self, student_id: int, selected_universities: list):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()
        
        applicant.selected_university_1 = selected_universities[0] 
        applicant.selected_university_2 = selected_universities[1]
        applicant.selected_university_3 = selected_universities[2]
        applicant.selected_university_4 = selected_universities[3]
        applicant.selected_university_5 = selected_universities[4]
        
        db.session.commit()
    
    def matchWithUniversity(self, student_id: int, university_id: int):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()
        applicant.matched_university = university_id
        db.session.commit()
    
    def getUniversitySelections(self, student_id: int):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()
        
        selections = []
        selections.append(applicant.selected_university_1)
        selections.append(applicant.selected_university_2)
        selections.append(applicant.selected_university_3)
        selections.append(applicant.selected_university_4)
        selections.append(applicant.selected_university_5)
        
        return selections
    
    def getMatchedUniversity(self, student_id: int):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()
        return applicant.matched_university
    
    def getMatchedUniversityName(self, student_id: int):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()
        matched_uni_id = applicant.matched_university
        uni = self.university_table.query.filter_by(university_id=matched_uni_id).first()
        if uni == None:
            uni_name = ""
        else:
            uni_name = uni.name
            
        return uni_name 
        
    def changeApplicationStatus(self, student_id: int, status: str):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()
        
        applicant.application_status = status
        
        db.session.commit()

    # def sendApplicationForm(self, id: int):
    #     application = self.application_table.query.filter_by(application_id = id).first()
    #     file = BytesIO(application.application_form) 
    #     return file

    # def sendPreapprovalForm(self, id: int): 
    #     application = self.application_table.query.filter_by(application_id = id).first()
    #     file = BytesIO(application.pre_approval_form) 
    #     if file == None:
    #         file = f"..\\forms\\signed_forms\\preapproval_form_{application.student_id}.pdf"
    #     return file

    # def sendLearningAgreementForm(self, id: int):
    #     application = self.application_table.query.filter_by(application_id = id).first()
    #     file = BytesIO(application.learning_agreement_form) 
    #     return file

    # def sendCourseTransfer(self, application_id : int):
    #     application = self.application_table.query.filter_by(application_id = application_id).first()
    #     file = BytesIO(application.final_transfer_form) 
    #     return file
    
    def uploadCourseTransfer(self, application_id: int, file):
        application = self.getApplicationById(application_id)
        application.final_transfer_form=file.read()
        application.application_status="under board inspection"
        db.session.commit()
        return application.final_transfer_form != None
    
    def deleteCourseTransfer(self, application_id: int):
        application = self.getApplicationById(application_id)
        application.final_transfer_form=None
        application.application_status="ready for mobility"
        db.session.commit()
        
    def getApplicationStatus(self, student_id: int):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()
        if applicant == None:
            new_application = self.application_table(student_id=student_id, application_status="not applied")
            db.session.add(new_application)
            db.commit()
            
            applicant = self.application_table.query.filter_by(student_id=student_id).first()
            
        status = applicant.application_status
        return status

    def addCourseSelection(self, student_id: int, courses: list):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()

        applicant.selected_courses = " ".join(courses)

        db.session.commit()
        
    def getSelectedCourses(self, student_id: int):
        applicant = self.application_table.query.filter_by(student_id=student_id).first()

        try:
            courses = applicant.selected_courses.split()
            dataCourses = [self.course_table.query.filter_by(course_name=course).first() for course in courses]
        except:
            dataCourses = []
            
        return dataCourses

    def download(self, student_id: int):
        application = self.application_table.query.filter_by(student_id=student_id).first()
        file_path = str(student_id) + "\\" + str(application.application_id) + ".pdf"
        return file_path

    def adjustStrategy(self, new_strategy:BaseDocumentStrategy):
        self.document_strategy = new_strategy

    def applyStrategy(self, id):
        return self.document_strategy.send_document(id)