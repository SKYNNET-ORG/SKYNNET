from flask import Flask, request, jsonify
from werkzeug.serving import WSGIRequestHandler

import subprocess 
application = Flask(__name__)


subproceso=None
@application.route("/START", methods=['GET', 'PUT', 'POST'])
def START():
    global subproceso
    if subproceso==None:
        subproceso=subprocess.Popen(['python', 'gui.py'], shell=False)
    return 'a'

@application.route("/STOP", methods=['GET', 'PUT', 'POST'])
def STOP():
    global subproceso
    subproceso.terminate()
    subproceso=None
    return 'b'

start_port_search=4998
if __name__ == '__main__':
	WSGIRequestHandler.protocol_version = "HTTP/1.1"
	#(local_port, sock) = get_port_available(port=start_port_search)
	#flask_thread = threading.Thread(target=flaskAppThreadFunction, args=[local_port, sock], daemon=False)
	#flask_thread.start()
	application.run(debug=False, host="0.0.0.0", port=4998, threaded=True)
	# Program name is not parameter