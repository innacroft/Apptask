from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user

from app.forms import LoginForm

from . import auth
from app.firestore_service import get_user
from app.models import UserModel, UserData

@auth.route('/login', methods= ['GET','POST'])
def login():
  login_form= LoginForm()
  context={
    'login_form': LoginForm()
  }
  if login_form.validate_on_submit():
    username=login_form.username.data 
    password=login_form.password.data

    
    user_doc=get_user(username)
    if user_doc.to_dict() is not None:
      password_from_db= user_doc.to_dict()['password']
      if password == password_from_db:
        flash('coindiden las contraseñas')
        user_data= UserData(username,password)
        user= UserModel(user_data)
        login_user(user)
        flash('bienvenido')
        return redirect(url_for('hello'))
      else:
        flash('Información no coincide')

    else:
      flash('Usuario no existe')



    return redirect(url_for('index'))


  return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout():
  logout_user()
  flash('regresa pronto')
  return redirect(url_for('auth.login'))