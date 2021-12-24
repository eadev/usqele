import pymysql.cursors

def start():
  # CONECTARSE A LA BASE DE DATOS
  connection = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               database=BD,
                               cursorclass=pymysql.cursors.DictCursor)

  with connection:  # SI SE CONECTO EJECUTA EL CÓDIGO SIGUIENTE
      with connection.cursor() as cursor: # SI PUEDE GENERAR EL CURSOS EJECUTA LO SIGUIENTE
          # Create a new record
          sql = "SHOW TABLES"
          cursor.execute(sql)
          tablas = cursor.fetchall()
          for tabla in tablas:
            print(f"{tabla['Tables_in_usqele']}")

if __name__ == '__main__':
  start()
