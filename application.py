# PAQUETES REQUERIDOS
import flask
from flask import Flask, render_template, request, session
import pymysql.cursors
import re
import logging
logging.basicConfig(filename='usqele.log', filemode='w', level=logging.DEBUG)

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
  # GENERAMOS EL LOG DE ACCESO
  logging.info(f'se ha conectado {USER}.' )  # will not print anything
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

@application.route("/dashboard", methods=['GET'])
def dashboard():
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
      #OBTENER LAS TABLAS DE LA BASE DE DATOS
      sql = f"SHOW FULL TABLES IN {DB} WHERE TABLE_TYPE LIKE 'BASE TABLE';"
      cursor.execute(sql)
      tablas = cursor.fetchall()
      ltablas = []
      for tabla in tablas:
        ltablas.append(f"{tabla['Tables_in_usqele']}")
      # OBTENER AS VISTAS DE LA BASE DE DATOS
      sql = f"SHOW FULL TABLES IN {DB} WHERE TABLE_TYPE LIKE 'VIEW';"
      cursor.execute(sql)
      vistas = cursor.fetchall()
      print(vistas)
      lvistas = []
      for vista in vistas:
        lvistas.append(f"{vista['Tables_in_usqele']}")
  return render_template('dashboard.html', tablas=ltablas, vistas=lvistas, basededatos=DB)


@application.route("/consulta", methods=['POST'])
def consulta():
  '''
  Permite la conexión a la base de datos.
  :return:
  '''
  HOST = session['host']
  USER = session['user']
  PASSWORD = session['password']
  DB = session['db']
  # CONECTARSE A LA BASE DE DATOS.
  connection = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               database=DB,
                               cursorclass=pymysql.cursors.DictCursor)
  with connection:  # SI SE CONECTO EJECUTA EL CÓDIGO SIGUIENTE
    with connection.cursor() as cursor:  # SI PUEDE GENERAR EL CURSOS EJECUTA LO SIGUIENTE
      sql = request.form.get("sql")
      cursor.execute(sql)
      data = cursor.fetchall()
      respuesta = "<TABLE class='table bg-white'>"
      for fila in data:
        respuesta = respuesta + "<TR>"
        for celda in fila:
          respuesta = respuesta + f"<TD colspan='2'>{fila[celda]}</TD>"
        respuesta = respuesta + "</TR>"
      respuesta = respuesta + "</TABLE>"
  return respuesta

@application.route("/salir", methods=['GET'])
def salir():
  session.clear()
  return flask.redirect("/login")

# SE EJECUTA CUANDO SE LLAMA ESTE ARCHIVO COMO PRINCIPAL
if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
