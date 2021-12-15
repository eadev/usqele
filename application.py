# PAQUETES REQUERIDOS
from flask import Flask, render_template

# GENERACIÓN DE LA APLICACIÓN FLASK
application = Flask(__name__)

# ENDPOINT DE LA APLICACIÓN
@application.route("/")
def home():
  '''
  Permite la conexión a la base de datos.
  :return:
  '''
  return render_template('index.html')


# ENDPOINT DE LA APLICACIÓN
@application.route("/login")
def login():
  '''
  Permite la conexión a la base de datos.
  :return:
  '''
  return render_template('login.html')


# ENDPOINT DE LA APLICACIÓN
@application.route("/signup")
def signup():
  '''
  Permite la conexión a la base de datos.
  :return:
  '''
  return render_template('signup.html')

@application.route("/dashboard")
def dashboard():
  '''
  Permite la conexión a la base de datos.
  :return:
  '''
  return render_template('dashboard.html')


# SE EJECUTA CUANDO SE LLAMA ESTE ARCHIVO COMO PRINCIPAL
if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
