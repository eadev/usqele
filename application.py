#!/usr/bin/python
# -*- coding: utf-8 -*-
import flask
from flask import Flask, render_template, request, session
import pymysql.cursors
import re
import logging
import traceback
logging.basicConfig(filename='./usqele.log', filemode='w', level=logging.DEBUG)

# GENERACIÓN DE LA APLICACIÓN FLASK
application = Flask(__name__)
application.secret_key = 'USQELE-SESSION'
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
  logging.info(f'se ha conectado {USER}.')
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
  connection.close()
  return flask.redirect("/dashboard")

@application.route("/dashboard", methods=['GET'])
def dashboard():
  if 'host' in session:
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
            i = 0
            for columna in tabla:
              if i == 0:
                ltablas.append(f"{tabla[columna]}")
              i += 1
          # OBTENER AS VISTAS DE LA BASE DE DATOS
          sql = f"SHOW FULL TABLES IN {DB} WHERE TABLE_TYPE LIKE 'VIEW';"
          cursor.execute(sql)
          vistas = cursor.fetchall()
          lvistas = []
          for vista in vistas:
            i = 0
            for columna in vista:
              if i == 0:
                lvistas.append(f"{vista[columna]}")
              i += 1
      connection.close()
      return render_template('dashboard.html', tablas=ltablas, vistas=lvistas, basededatos=DB)
  else:
    return flask.redirect("/login")


@application.route("/consulta", methods=['POST'])
def consulta():
  '''
  Permite la conexión a la base de datos.
  :return:
  '''
  try:
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
        sentencias_tipo = ['CREATE', 'UPDATE', 'INSERT', 'DELETE']
        band = 0
        for sentencia in sentencias_tipo:
          if sentencia in sql or sentencia.upper() in sql:
            band = 1
        # EJECUTAMOS LA SENTENCIA SQL
        afectadas = cursor.execute(sql)
        if band == 0:
          data = cursor.fetchall()
          respuesta = "<TABLE class='table table-bordered table-striped'>"
          band = 0
          if len(data) > 0:
            for fila in data:

              if band == 0:
                respuesta = respuesta + "<THEAD><TR>"
                for celda in fila:
                  respuesta = respuesta + f"<TH>{celda}</TH>"
                respuesta = respuesta + "</TR></THEAD><TBODY>"
              respuesta = respuesta + "<TR>"
              for celda in fila:
                respuesta = respuesta + f"<TD>{fila[celda]}</TD>"
              respuesta = respuesta + "</TR>"
              band = 1
            respuesta = respuesta + "</TBODY></TABLE>"
          else:
            respuesta = "<div class='alert alert-warning text-center'>No se han retornado datos.</div>"
        else:
          connection.commit()
          respuesta = f"<div class='alert alert-warning text-center'>Se han afecta {afectadas} filas.</div>"
    connection.close()
    return respuesta
  except pymysql.Error as error:
    code, message = error.args
    error = f"Código: <b>{code}</b>: <i>{message}</i>"
    respuesta = f"<div class='alert alert-danger text-center'><b> Error en la sentencia </b> >> {error}</div>"
    return respuesta

@application.route("/salir", methods=['GET'])
def salir():
  session.clear()
  return flask.redirect("/login")

# SE EJECUTA CUANDO SE LLAMA ESTE ARCHIVO COMO PRINCIPAL
if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
