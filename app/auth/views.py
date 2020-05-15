from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm

from . import auth
from app.firestore_service import get_user,user_put
from app.models import UserModel, UserData


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)
        
        
        if user_doc.to_dict() is not None:
            #password_from_db = user_doc.to_dict()['password']

            if check_password_hash(user_doc.to_dict()['password'], password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                print(f'-user: {user}')
                status=login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('La información no coincide')
        else:
          flash('El usario no existe')
        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('signup', methods=['GET','POST'])
def signup():
  signup_form=LoginForm()
  context={
    'signup_form':signup_form
  }
  if signup_form.validate_on_submit():
    username=signup_form.username.data
    password=signup_form.password.data
    user_doc=get_user(username)
    print(user_doc)
    if user_doc.to_dict() is None:
      password_hash= generate_password_hash(password)
      user_data= UserData(username,password_hash)
      user_put(user_data)
      user= UserModel(user_data)
      login_user(user)
      flash('Bienvenido')
      
      return redirect(url_for('hello'))
    else:
      flash('el usuario ya existe! ')

  return render_template('signup.html',**context)

@auth.route('logout')
@login_required
def logout():
  logout_user()
  flash('regresa pronto')
  return redirect(url_for('auth.login'))