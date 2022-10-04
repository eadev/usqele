import os
import os.path
from dotenv import load_dotenv
import logging

# SET THE LOG PATH
ruta_base = os.path.dirname(__file__)
logging.basicConfig(filename=ruta_base+'/../logs/application.log', level=logging.DEBUG)

class Startup:
    def iniciar(self):
        dir = os.path.dirname(__file__)
        if os.path.isfile(dir+'/.env'):
          env_path = dir+'/.env'
          load_dotenv(dotenv_path=env_path)
# START CODE
ostartup = Startup()
ostartup.iniciar()