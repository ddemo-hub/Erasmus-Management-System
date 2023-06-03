from flask import render_template, request, redirect, url_for

from flask.views import MethodView


class Main(MethodView):
    def __init__(self, university_service):
        self.university_service = university_service


    def get(self):
        university_list = self.university_service.getAllUniversities()
        university_list_checked = []
        for university in university_list:
            if university.image_url == None:
                university.image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/640px-Image_not_available.png"
            university_list_checked.append(university)
        
        return render_template("main_page.html", boolean=True, university_list = university_list_checked)
    
    
