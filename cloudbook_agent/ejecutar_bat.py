import subprocess
import threading
import time
import sys
import psutil

import signal


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
class HiloEjecutarBat(threading.Thread):
    def __init__(self):
        super().__init__()
        self.subproceso=None
    
    def run(self):
        try:
            self.subproceso=subprocess.Popen(['python', 'C:\\Users\\gomezbot\\Desktop\\sk_cloudbook-main\\cloudbook_agent\\gui.py'], shell=False)
            
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el archivo .bat: {e}")
    def detener(self):
        kill_process(self.subproceso)
        
    def hola (self):
        print('hola')


# Ejemplo de uso
if __name__ == "__main__":
    ruta_archivo_bat = "C:\\dashboard\\ejecutar_py.bat"
    parametro_a_pasar=""
    with open("config.txt", "r") as archivo:
        for linea in archivo:
            parametro_a_pasar=linea
    print(parametro_a_pasar)
    """hola=HiloEjecutarBat(ruta_archivo_bat, parametro_a_pasar)
    hola.run()
    import time
    time.sleep(3)
    print('hola')
    hola.detener()
    time.sleep(5)
    print('acabo')"""
    """
    subproceso=subprocess.Popen(['python', 'C:\\Users\\gomezbot\\Desktop\\sk_cloudbook-main\\cloudbook_agent\\gui.py'], shell=False)
    print(subproceso.pid)
    time.sleep(5)
    subproceso.terminate()
    """
    hola=HiloEjecutarBat()
    hola.run()
    time.sleep(5)
    hola.detener()
    print('terminado')
    try:    
        while True:        
            pass 
    except KeyboardInterrupt:    
        print("Se presionó Ctrl+C. Saliendo del bucle.")
