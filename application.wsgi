#! /usr/bin/python3
import logging
import sys
import pathlib

logging.basicConfig(stream=sys.stderr)
ruta_base = str(pathlib.Path(__file__).parent.absolute())+"/"
sys.path.insert(0, str(ruta_base))
from application import application as application
application.secret_key = 'KEY-WSFLASK-24680'
