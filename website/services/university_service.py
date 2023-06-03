from .singleton import Singleton
from website import db

class UniversityService(metaclass=Singleton):
    def __init__(self, university_table, university_departments_table):
        self.university_table = university_table
        self.university_departments_table = university_departments_table
        
    def getAllUniversities(self):
        all_data = self.university_table.query.all()
        return all_data

    def getUniversityById(self, id):
        university = self.university_table.query.filter_by(university_id = id).first()
        return university

    def addUniversity(self, name: str, country: str, semester: str, department: str, language: str, quota: int):
        new_university = self.university_table(
            name = name,
            country = country,
            semester = semester,
            language_requirements = language,
            image_url = None
        )
        db.session.add(new_university)
        db.session.commit()
        self.addDepartment(
            department = department,
            quota = quota,
            university_id = new_university.university_id
        )
        return new_university

    def addDepartment(self, department: str, quota: int, university_id: int):
        new_department = self.university_departments_table(
            department = department,
            total_quota = quota,
            remaining_quota = quota,
            university_id = university_id
        )
        db.session.add(new_department)
        db.session.commit()
        return new_department

    def updateUniversity(self, id: int, name: str, country: str, semester: str, department: str, language: str, total_quota: int, remaining_quota: int):
        university = self.getUniversityById(id)
        university.name = name
        university.country = country
        university.semester = semester
        university.language_requirements = language
        db.session.commit()
        self.updateDepartment(department=department, total_quota=total_quota, remaining_quota=remaining_quota, university_id=id)
        return university
    
    def updateDepartment(self, department: str, total_quota: int, remaining_quota: int, university_id: int):
        department = self.getDepartment(department=department, university_id=university_id)
        department.total_quota = total_quota
        department.remaining_quota = remaining_quota
        db.session.commit()
        return department
    
    def getUniversitiesByDepartment(self, department: str):
        university_ids = self.university_departments_table.query.filter_by(department=department).all()
        universities = [self.university_table.query.filter_by(university_id=id.university_id).first() for id in university_ids] 
        return universities

    def getUniversityByName(self, name: str):
        university = self.university_table.query.filter_by(name=name).first()
        return university

    def getDepartments(self, department: str):
        departments = self.university_departments_table.query.filter_by(department=department).order_by(self.university_departments_table.university_id).all()
        return departments
    
    def getDepartment(self, department: str, university_id: int):
        department = self.university_departments_table.query.filter_by(department=department, university_id=university_id).first()
        return department
