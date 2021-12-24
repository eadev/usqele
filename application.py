# PAQUETES REQUERIDOS
import flask
from flask import Flask, render_template, request, session
import pymysql.cursors

# GENERACIÓN DE LA APLICACIÓN FLASK
application = Flask(__name__)
application.secret_key = 'USQELE-KEY-12412'
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


@application.route("/conectar", methods=['POST'])
def conectar():
  HOST = request.form.get("host")
  USER = request.form.get("user")
  PASSWORD = request.form.get("password")
  DB = request.form.get("bd")

  # CONECTARSE A LA BASE DE DATOS
  connection = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               database=DB,
                               cursorclass=pymysql.cursors.DictCursor)

  with connection:  # SI SE CONECTO EJECUTA EL CÓDIGO SIGUIENTE
      with connection.cursor() as cursor: # SI PUEDE GENERAR EL CURSOS EJECUTA LO SIGUIENTE
          session['host'] = HOST
          session['user'] = USER
          session['password'] = PASSWORD
          session['db'] = DB

  return flask.redirect("/dashboard")

@application.route("/dashboard")
def dashboard():
  '''
  Permite la conexión a la base de datos.
  :return:
  '''
  HOST = session['host']
  USER = session['user']
  PASSWORD = session['password']
  DB = session['db']
  # CONECTARSE A LA BASE DE DATOS
  connection = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               database=DB,
                               cursorclass=pymysql.cursors.DictCursor)

  with connection:  # SI SE CONECTO EJECUTA EL CÓDIGO SIGUIENTE
    with connection.cursor() as cursor:  # SI PUEDE GENERAR EL CURSOS EJECUTA LO SIGUIENTE
      sql = "SHOW TABLES"
      cursor.execute(sql)
      tablas = cursor.fetchall()
      ltablas = []
      for tabla in tablas:
        ltablas.append(f"{tabla['Tables_in_usqele']}")
  return render_template('dashboard.html', tablas=ltablas, basededatos=DB)


def sumar(a, b):
  return a + b

# SE EJECUTA CUANDO SE LLAMA ESTE ARCHIVO COMO PRINCIPAL
if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
