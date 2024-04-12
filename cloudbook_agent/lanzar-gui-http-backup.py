from flask import Flask, request
from flask import jsonify
from werkzeug.serving import WSGIRequestHandler
import threading
import socket
import subprocess as sp
import loader		
import sys
application = Flask(__name__)
import subprocess
import psutil 

class HiloEjecutarBat(threading.Thread):
    def __init__(self, ruta_bat, parametro):
        super().__init__()
        self.ruta_bat = ruta_bat
        self.parametro = parametro
        self.run()

    def run(self):
        try:
            self.subproceso=subprocess.Popen([self.ruta_bat, self.parametro], shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el archivo .bat: {e}")
    def detener(self):
        #self.subproceso.terminate()
        pid=os.getpid()
        process=psutil.Process(pid)
        process.terminate()
    def hola (self):
        print('hola')
    def getpid(self):
        return self.subproceso.pid

import platform, os, signal
def kill_process(proc):
	if platform.system()=="Windows":
		# proc.send_signal(signal.CTRL_BREAK_EVENT)
		# proc.kill()
		kill_tree_command = "TASKKILL /F /T /PID "+str(proc.pid)
		kill_tree_command += " > NUL 2>&1"
		os.system(kill_tree_command)	
	else:
		try:
			os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
		except Exception as e:
			print(e)


subproceso=None
ruta_gui=""
@application.route("/START", methods=['GET', 'PUT', 'POST'])
def START():
    global subproceso
    global ruta_gui
    with open("config.txt", "r") as archivo:
        for linea in archivo:
            ruta_gui+=linea
    print(ruta_gui)
    #hola=HiloEjecutarBat(ruta_archivo_bat, parametro_a_pasar)
    subproceso=subprocess.Popen(['python', ruta_gui+'\\gui.py'], shell=False)
    print(subproceso.pid)
    return 'a'



@application.route("/STOP", methods=['GET', 'PUT', 'POST'])
def STOP():
    global subproceso
    subproceso.terminate()
    #pid = psutil.Process(__name__="CLOUDBOOK_agent_0_(boinc)").pid()
    #psutil.Process(__name__="")
    #print(pid)
    import time 
    time.sleep(5)
    #kill_process(subproceso)
    return 'b'

start_port_search=4998
if __name__ == '__main__':
	WSGIRequestHandler.protocol_version = "HTTP/1.1"
	#(local_port, sock) = get_port_available(port=start_port_search)
	#flask_thread = threading.Thread(target=flaskAppThreadFunction, args=[local_port, sock], daemon=False)
	#flask_thread.start()
	application.run(debug=False, host="0.0.0.0", port=4998, threaded=True)
	# Program name is not parameter