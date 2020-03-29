from flask import Flask,request, make_response, redirect

app= Flask(__name__) #aca se pone el nombre del app

@app.route():
def index():
  user_ip = request.remote_addr
  response= make_response(redirect('/hello'))
  response.set_cookie=('user_ip',user_ip)
  return response




@app.route('/') #la ruta donde se va a ejecutar la funcion
def hello():
  user_ip = request.cookies.get('user_ip')
  return 'hello world Flask, tu ip es {}'.format(user_ip)
