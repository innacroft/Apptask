from flask_testing import TestCase
from flask import current_app,url_for
from main import app
import sys

class MainTest(TestCase):
  print(sys.path)
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
    response = self.client.post(url_for('hello'))
    self.assertTrue(response.status_code,405)
  
  def test_auth_blueprint_exists(self):
    self.assertIn('auth',self.app.blueprints)

  def test_auth_login_get(self):
    response= self.client.get(url_for('auth.login'))
    self.assert200(response)
  
  def test_auth_login_template(self):
    self.client.get(url_for('auth.login'))
    self.assertTemplateUsed('login.html')

  def test_auth_login_post(self):
    fake_form={
      'username':'fake',
      'password':'fake-password'
    }
    response=self.client.post(url_for('auth.login'),data= fake_form)
    self.assertRedirects(response,url_for('index'))