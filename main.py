from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest

from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users, get_todos
from flask_login import login_required, current_user
app = create_app()

todos=['Comprar cafe', 'Enviar solicitud de compra','Entregar video al productor']

@app.cli.command() #crea commando con click para crear los tests
def test():
  tests= unittest.TestLoader().discover('tests')
  unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error)

@app.errorhandler(500)
def no_server(error):
  return render_template('500.html', error=error)  

@app.route('/')
def index():
  user_ip = request.remote_addr
  response = make_response(redirect('/hello'))
  #response.set_cookie('user_ip', user_ip)
  session['user_ip']=user_ip
  return response

@app.route('/hello', methods=['GET','POST'])
@login_required
def hello():
#creamos nueva variable de la ip que detectamos en el browser

  #user_ip = request.cookies.get('user_ip')
  user_ip= session.get('user_ip')
  username= current_user.id
  username= session.get('username')
  context={
    'user_ip':user_ip,
    'todos':get_todos(user_id=username),
    'username':username
  }

  return render_template('hello.html', **context)


if __name__ == "__main__":
    app.run(debug=True)