from flask import Flask, request, make_response, redirect, render_template,session
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

#inicializacion de librerias
bootstrap= Bootstrap(app)

app.config['SECRET_KEY']='SUPER SECRETO'

todos=['Comprar cafe', 'Enviar solicitud de compra','Entregar video al productor']

class LoginForm(FlaskForm):
  username=StringField('Nombre de usuario',validators=[DataRequired()])
  password=PasswordField('Password',validators=[DataRequired()])
  submit= SubmitField('Enviar')




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

@app.route('/hello')
def hello():
#creamos nueva variable de la ip que detectamos en el browser

  #user_ip = request.cookies.get('user_ip')
  user_ip= session.get('user_ip')
  login_form= LoginForm()
  context={
    'user_ip':user_ip,
    'todos':todos,
    'login_form':login_form
  }

  return render_template('hello.html', **context)

if __name__ == "__main__":
    app.run(debug=True)