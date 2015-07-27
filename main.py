import webapp2
import jinja2
import os
import logging
import urllib
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Student(ndb.Model):
	first_name = ndb.StringProperty(indexed=True)
	last_name = ndb.StringProperty(indexed=True)
	age = ndb.IntegerProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

class CreateStudentPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render())
    def post(self):
        student = Student()
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.age = int(self.request.get('age'))
        student.put()
        self.redirect('#regDone')

class SuccessPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Success! <a href="/student/list">view students</a>')

class StudentList(webapp2.RequestHandler):
    def get(self):
    	students = Student.query().order(-Student.date).fetch()
    	logging.info(students)
        template_data = {
            'student_list': students
        }
        template = JINJA_ENVIRONMENT.get_template('list.html')
        self.response.write(template.render(template_data)) 

class  StudentEdit(webapp2.RequestHandler):
    def get(self,stud_id):
        s = Student.get_by_id(int(stud_id))
        template_data = {
            'student': s
        }
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_data))
    def post(self,stud_id):
        s = Student.get_by_id(int(stud_id))
        s.first_name = self.request.get('first_edit')
        s.last_name = self.request.get('last_edit')
        s.age = int(self.request.get('age_edit'))
        s.put()
        self.redirect('#regDone')

class  StudentPage(webapp2.RequestHandler):
    def get(self,stud_id):
        s = Student.get_by_id(int(stud_id))
        template_data = {
            'student': s
        }
        template = JINJA_ENVIRONMENT.get_template('studPage.html')
        self.response.write(template.render(template_data))

class  StudentDelete(webapp2.RequestHandler):
    def get(self,stud_id):
        d = Student.get_by_id(int(stud_id))
        d.key.delete()
        self.redirect('/delete')
        
class DeletePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Delete Success! <a href="/student/list">view students</a>')

app = webapp2.WSGIApplication([
    ('/student/create', CreateStudentPage),
    ('/student/edit/(.*)',StudentEdit),
    ('/student/delete/(.*)',StudentDelete),
    ('/', MainPage),
    ('/student/list', StudentList),
    ('/success', SuccessPage),
    ('/delete', DeletePage),
    ('/student/page/(.*)', StudentPage)
], debug=True)