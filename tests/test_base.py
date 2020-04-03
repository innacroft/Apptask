from flask_testing import TestCase
from flask import current_app,url_for
from main import app

class MainTest(TestCase):
  def create_app(self):
    app.config['TESTING']=True
    app.config['WTF_CSRF_ENABLED']=False
    return app

  def test_app_exists(self): #app existe
    self.assertIsNotNone(current_app) 
  
  def test_app_in_test_mode(self): #app esta en testing
    self.assertTrue(current_app.config['TESTING'])
  
  def test_index_redirects(self):  #verificar que el index si redirige a hello
    response= self.client.get(url_for('index'))
    self.assertRedirects(response, url_for('hello'))

  def test_hello_get(self): #hello regresa 200 cuando se hace get
    response= self.client.get(url_for('hello'))
    self.assert200(response)
  
  def test_hello_post(self): #hello verificacion de  post
    fake_form={
      'username':'fake' ,
      'password': 'fake-passw'
    }
    response = self.client.post(url_for('hello'), data=fake_form)
    self.assertRedirects(response,url_for('index'))