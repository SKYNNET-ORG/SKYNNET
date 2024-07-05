
from enum import Enum
import os, sys, platform
				# In project directory
import requests
from colorama import init, Fore, Back, Style
import time
import dearpygui.dearpygui as dpg
import psutil
import threading
import subprocess 

projects={}
class project:
	def __init__(self,nombre, gui):
		self.agents={}
		self.gui=gui
		self.name=nombre
		#cambiar esta linea
		for x in self.gui:
			url=str(x)+'/info/'+str(self.name)
			respuesta = requests.get(url)
			if respuesta.status_code==200:
				aux = respuesta.json()
				for clave, valor in aux.items():
					self.agents[valor['AGENT_ID']]=agents(valor['AGENT_ID'],valor['GRANT_LEVEL'],x,valor['lanzado'])

		#def __init__(self,id,level,ip,status='sin señal'):				
		"""
		all_files = next(os.walk(agents_path))[2]

		
		# Cleaning. If file does not contain "config_" it is not an agent config file.
		files = [file for file in all_files if  "config_agent_" in file and \
												"config_agent_"==file[:13] and \
												".json" in file and \
												".json"==file[-5:]]
		aux={}
		for file in files:
			aux[files.index(file)] = loader.load_dictionary(agents_path + os.sep + file)

		#{'AGENT_ID': 'agent_0', 'GRANT_LEVEL': 'MEDIUM', 'DISTRIBUTED_FS': 'C:\\Users\\gomezbot\\cloudbook\\boinc\\distributed'}

		"""
			


	def añadir_agente(self,level,IsAgent0,gui):
		if IsAgent0==True:
			IsAgent0=1
		else:
			IsAgent0=0
		if isinstance(gui, str):
			url=str(gui)+'/create/'+str(self.name)+'/'+str(level)+'/'+str(IsAgent0)
		else:
			url=str(self.gui[gui])+'/create/'+str(self.name)+'/'+str(level)+'/'+str(IsAgent0)
		respuesta = requests.get(url)
		if respuesta.status_code == 200:
			if isinstance(gui, str):
				self.agents[respuesta.text]=agents(respuesta.text,Grant_level(level),gui,'parado')
			else:
				self.agents[respuesta.text]=agents(respuesta.text,Grant_level(level),self.gui[gui],'parado')
			
			return respuesta.text
		

	def eliminar_agentes(self, id ):
		url=str(self.agents[id].ip)+'/remove/'+str(self.name)+'/'+str(id)
		respuesta = requests.get(url)
		if respuesta.status_code == 200:
			del self.agents[id]

	def lanzar_agentes(self, id):
		url=str(self.agents[id].ip)+'/Launch/'+str(self.name)+'/'+str(id)
		respuesta = requests.get(url)
		if respuesta.status_code == 200:
			self.agents[id].cambiar_estado('lanzado')

	def parar_agentes(self,id):
		url=str(self.agents[id].ip)+'/stop/'+str(self.name)+'/'+str(id)
		respuesta = requests.get(url)
		if respuesta.status_code == 200:
			self.agents[id].cambiar_estado('parado'	)

	def save_change(self, id, grant):
		url=str(self.agents[id].ip)+'/edit/'+str(self.name)+'/'+str(id)+'/'+str(grant)
		respuesta = requests.get(url)
		if respuesta.status_code == 200:
			self.agents[id].editar(grant)

	def agentes(self):
		x=0
		for clave, valor in self.agents.items():
			sys.stdout.flush()
			x+=1
	def numGui(self):
		return len(self.gui)

	def __str__(self):
		return 'name: '+str(self.name)+' agents '+str(self.agents)
class Opciones(Enum):
    lanzado = 'lanzado'
    parado = 'parado'
    sin_señal = 'sin señal'


class Grant_level(Enum):
    MEDIUM = 1
    LOW =2
    HIGH =0

Grant=['HIGH','MEDIUM','LOW']

def obtener_nivel(estado):
    if estado == "MEDIUM":
        return Grant_level.MEDIUM
    elif estado == "LOW":
        return Grant_level.LOW
    elif estado == "HIGH":
        return Grant_level.HIGH
    else :
    	return estado # Manejar un estado no válido

class agents: 
	def __init__(self,id,level,ip,status='sin señal'):
		self.id=id
		self.status=Opciones(status)
		self.Grant_level=obtener_nivel(level)
		self.ip=ip
	def cambiar_estado(self,status):
		self.status=Opciones(status)
	def editar(self,grant):
		self.Grant_level=obtener_nivel(Grant[grant])
	def __str__(self):
		
		id_str = Fore.BLUE + str(self.id)
		estado = self.status.value
		if estado == 'lanzado':
			estado_str = Fore.GREEN + str(estado)
		elif estado == 'parado':
			estado_str = Fore.RED + str(estado)
		else: #estado == 'sin señal':
			estado_str = Fore.LIGHTBLACK_EX + str(estado)
        
		return id_str + ' ' + estado_str + ' ' +Fore.RESET+ str(Grant[self.Grant_level.value]) + ' '+self.ip[:-5]
	

projects_list={}
with open("gui.txt", "r") as archivo:
	for linea in archivo:
		url=str(linea).replace("\n", "")+':4998'+'/START'
		print(url)
		linea=linea.replace("\n", "")+':4999'


		respuesta = requests.get(url)
		#respuesta.status_code==200



		time.sleep(1)
		recibido=0
		if respuesta.status_code == 200:
			url=str(linea)+'/projects'
			while recibido<5:
				try:
					respuesta = requests.get(url)
					recibido=6
				except:
					recibido=0
			if respuesta.status_code == 200:
				x=respuesta.text.split('"')
				for i in range(1,len(x)-1,2):
					try:
						projects_list[x[i]].append(linea)
					except:
						projects_list[x[i]]=[linea]
projects_list


for x in projects_list:
	gui=projects_list[x]
	projects[x]=project(x,gui)

projects_list=list(projects_list.keys())


#gui aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa


rojo=[200, 0, 0]
verde=[0, 200, 0]





global proyecto 

dpg.create_context()
def on_dropdown_selection3(sender, app_data):
	print(f"Seleccionaste: {app_data}")



def on_dropdown_selection2(sender=None, app_data=None):
	global proyecto
	gui=dpg.get_value('combo_guis')
	print(gui)
	objetos_con_estado =[agente_id for agente_id, agente in proyecto.agents.items() if (agente.status == Opciones.lanzado and agente.ip==gui)]
	
	agentes = objetos_con_estado
	if len(agentes)!=0:
			agentes.append('todos')
	else:
		agentes.append('no hay agentes lanzados')
	try:
		dpg.delete_item("combo_agents")
		dpg.delete_item('text_agentes')
	except:
		pass
	dpg.add_text('Elige un agente', parent='combos',tag='text_agentes')
	dpg.add_combo( items=agentes,parent="combos", tag="combo_agents",callback=on_dropdown_selection3)

	
def on_dropdown_selection(sender, app_data):
	print(f"Seleccionaste: {app_data}")
	global proyecto
	proyecto=projects[app_data]
	try:
		dpg.delete_item("combo_agents")
		dpg.delete_item('text_agentes')
		dpg.delete_item('combo_guis')
		dpg.delete_item('textogui')
	except:
		pass
	dpg.add_text('Elige un ordenador', parent='combos',tag='textogui')
	dpg.add_combo( items=proyecto.gui,parent="combos", tag="combo_guis",callback=on_dropdown_selection2)
	manage1(proyecto)


def proceso_Deploy():
	global proyecto
	
	try:
		full_command='start \"deploy\" py C:/Users/gomezbot/Desktop/sk_cloudbook-main/cloudbook_deployer/cloudbook_deployer.py -project_folder '+str(proyecto.name)
		subprocess.Popen(full_command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
	except Exception as e:
		print(e)


"""
def button_deploy():
	update_thread = threading.Thread(target=proceso_Deploy)
	
	update_thread.start()
	"""
def proceso_run():
	global proyecto
	try:
		full_command='start \"run\" py C:/Users/gomezbot/Desktop/sk_cloudbook-main/cloudbook_deployer/cloudbook_run.py -project_folder '+str(proyecto.name)
		subprocess.Popen(full_command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
	except Exception as e:
		print(e)


"""def button_run():
	update_thread = threading.Thread(target=proceso_run)
	update_thread.start()"""
	



#dpg.add_handler_registry(tag="global")
dpg.add_window(label="ventana principal",tag="ventana")
dpg.add_group(horizontal=True,parent='ventana',tag='grupo')
dpg.add_child_window(tag='vertical',width=700,parent='grupo')


dpg.add_group(horizontal=False,parent='vertical',tag='grupovertical')
dpg.add_child_window(tag='ventana_principal', height=200,parent='grupovertical')
dpg.add_group(horizontal=False,parent='ventana_principal',tag='combos')
dpg.add_group(horizontal=True,parent='ventana_principal',tag='botones')
dpg.add_text('Elige un Proyecto', parent="combos")
dpg.add_combo( items=projects_list, parent="combos",tag='proyecto',callback=on_dropdown_selection)
#dpg.add_button(label='Desplegar', parent="botones",tag='Deploy',callback=proceso_Deploy)
#dpg.add_button(label='Ejecutar proyecto', parent="botones",tag='run_proyecto',callback=proceso_run)
#dpg.add_child_window(  parent='grupo')

######################################crear manage
def lanzar(sender, app_data):

	button_data = dpg.get_item_user_data(sender)
	
	projects[button_data[0]].lanzar_agentes(button_data[1])
	text_id = ("status_"+str(button_data[1]))

	dpg.set_value("status_"+str(button_data[0])+str(button_data[1]),projects[button_data[0]].agents[button_data[1]].status.value  )
	if dpg.does_item_exist("combo_agents")==True:
		on_dropdown_selection2()
def parar(sender, app_data):

	button_data = dpg.get_item_user_data(sender)
	
	projects[button_data[0]].parar_agentes(button_data[1])

	print(projects[button_data[0]].agents[button_data[1]].status)
	text_id = ("status_"+str(button_data[1]))
	print(text_id)
	dpg.set_value("status_"+str(button_data[0])+str(button_data[1]),projects[button_data[0]].agents[button_data[1]].status.value )
	if dpg.does_item_exist("combo_agents")==True:
		on_dropdown_selection2()
def eliminar(sender, app_data):

	button_data = dpg.get_item_user_data(sender)
	
	projects[button_data[0]].eliminar_agentes(button_data[1])
	dpg.delete_item(str(button_data[0])+str(button_data[1]))

def añadir_agent(sender, app_data):
	button_data = dpg.get_item_user_data(sender)
	combo1_text = dpg.get_value('gui')
	combo2_text = dpg.get_value('level')
	level=obtener_nivel(combo2_text)
	checkbox = dpg.get_value('isagent0')
	agent_id=projects[button_data[0]].añadir_agente(level.value,checkbox,combo1_text)
	dpg.delete_item("añadir")
	x=button_data[0]
	agente=projects[button_data[0]].agents[agent_id]
	agente_id=agente.id
	dpg.add_table_row(parent='table_'+str(x),tag=str(x)+str(agente_id))
	dpg.add_text(str(agente.id),parent=str(x)+str(agente_id))
	dpg.add_text(str(agente.status.value),parent=str(x)+str(agente_id),tag='status_'+str(x)+str(agente_id))
	dpg.add_text(str(agente.ip),parent=str(x)+str(agente_id))
	dpg.add_text(str(Grant[agente.Grant_level.value]),parent=str(x)+str(agente_id))
	dpg.add_table_cell(parent=str(x)+str(agente_id),tag='botones'+str(x)+str(agente_id))
	dpg.add_button(label='lanzar',user_data=[x,agente.id],parent='botones'+str(x)+str(agente_id),callback=lanzar)
	dpg.add_same_line(parent='botones'+str(x)+str(agente_id))
	dpg.add_button(label='parar',user_data=[x,agente.id],parent='botones'+str(x)+str(agente_id),callback=parar)
	dpg.add_same_line(parent='botones'+str(x)+str(agente_id))
	dpg.add_button(label='eliminar',user_data=[x,agente.id],parent='botones'+str(x)+str(agente_id),callback=eliminar)


#def añadir_agente(self,level,IsAgent0,gui):


def añadir(sender, app_data):
	button_data = dpg.get_item_user_data(sender)
	dpg.add_window(label="ExampleWindow",tag="añadir",id="añadir")
	dpg.add_combo( items=['HIGH','MEDIUM','LOW'], parent="añadir",tag='level')
	dpg.add_combo( items=projects[button_data[0]].gui, parent="añadir",tag='gui')
	dpg.add_checkbox(label='is agent 0',parent="añadir",tag='isagent0')
	dpg.add_button(label="añadir",user_data=[button_data[0]], callback=añadir_agent,parent="añadir")


def manage1(project):
	try:
		dpg.delete_item("ventana_agentes")
	except:
		pass
	ventana_existe = dpg.does_item_exist("ventana_agentes")
	print(f"¿La ventana existe? {ventana_existe}")
	if ventana_existe==False:
		dpg.add_child_window(tag="ventana_agentes",parent='grupovertical')

		dpg.add_button(label='añadir',user_data=[project.name],parent="ventana_agentes",callback=añadir)
		dpg.add_table(header_row=True ,tag='table_'+str(project.name),parent="ventana_agentes",
						   borders_outerH=True, borders_innerV=True, borders_outerV=True)
			#dpg.add_table_column(label='hola',parent='table_'+str(project.name))     label='agent_id',
		
		dpg.add_table_column(label='id',parent='table_'+str(project.name))
		dpg.add_table_column(label='status',parent='table_'+str(project.name),init_width_or_weight=0.3)
		dpg.add_table_column(label='gui',parent='table_'+str(project.name),init_width_or_weight=0.7)
		dpg.add_table_column(label='grant',parent='table_'+str(project.name),init_width_or_weight=0.2)
		dpg.add_table_column(label='botons',parent='table_'+str(project.name))
		for agente_id, agente in project.agents.items():
			dpg.add_table_row(parent='table_'+str(project.name),tag=str(project.name)+str(agente_id))
			if agente.status.value=='lanzado':
				dpg.add_text(str(agente.id),parent=str(project.name)+str(agente_id))
				dpg.add_text(str(agente.status.value),parent=str(project.name)+str(agente_id),tag='status_'+str(project.name)+str(agente_id))
				
				dpg.add_text(str(agente.ip),parent=str(project.name)+str(agente_id))
				dpg.add_text(str(Grant[agente.Grant_level.value]),parent=str(project.name)+str(agente_id))
			else:
				dpg.add_text(str(agente.id),parent=str(project.name)+str(agente_id))
				dpg.add_text(str(agente.status.value),parent=str(project.name)+str(agente_id),tag='status_'+str(project.name)+str(agente_id))
				dpg.add_text(str(agente.ip),parent=str(project.name)+str(agente_id))
				
				dpg.add_text(str(Grant[agente.Grant_level.value]),parent=str(project.name)+str(agente_id))
				
			dpg.add_table_cell(parent=str(project.name)+str(agente_id),tag='botones'+str(project.name)+str(agente_id))
			with dpg.group(horizontal=True, parent='botones'+str(project.name)+str(agente_id)):
				dpg.add_button(label='lanzar',user_data=[project.name,agente.id],callback=lanzar)

				dpg.add_button(label='parar',user_data=[project.name,agente.id],callback=parar)

				dpg.add_button(label='eliminar',user_data=[project.name,agente.id],callback=eliminar)
	else:
		dpg.show_item('ventana_agentes')




def manage(sender, app_data):
	ventana_existe = dpg.does_item_exist("ventana_agentes")
	print(f"¿La ventana existe? {ventana_existe}")
	if ventana_existe==False:
		dpg.add_child_window(tag="ventana_agentes",parent='grupovertical')
		dpg.add_tab_bar(tag='menuproyectos',parent='ventana_agentes')
		for x in projects_list:
			dpg.add_tab(label=x,tag='notebook_'+str(x),parent='menuproyectos')
			dpg.add_button(label='añadir',user_data=[x],parent='notebook_'+str(x),callback=añadir)
			dpg.add_table(header_row=True ,tag='table_'+str(x),parent='notebook_'+str(x),
						   borders_outerH=True, borders_innerV=True, borders_outerV=True)
			proyecto=projects[x]
			#dpg.add_table_column(label='hola',parent='table_'+str(x))     label='agent_id',
			dpg.add_table_column(label='id',parent='table_'+str(x))
			dpg.add_table_column(label='status',parent='table_'+str(x),init_width_or_weight=0.3)
			dpg.add_table_column(label='gui',parent='table_'+str(x),init_width_or_weight=0.7)
			dpg.add_table_column(label='grant',parent='table_'+str(x),init_width_or_weight=0.2)
			dpg.add_table_column(label='botons',parent='table_'+str(x))
			for agente_id, agente in proyecto.agents.items():
				dpg.add_table_row(parent='table_'+str(x),tag=str(x)+str(agente_id))
				if agente.status.value=='lanzado':
					dpg.add_text(str(agente.id),parent=str(x)+str(agente_id))
					dpg.add_text(str(agente.status.value),parent=str(x)+str(agente_id),tag='status_'+str(x)+str(agente_id))
					dpg.add_text(str(agente.ip),parent=str(x)+str(agente_id))
					dpg.add_text(str(Grant[agente.Grant_level.value]),parent=str(x)+str(agente_id))
				else:
					dpg.add_text(str(agente.id),parent=str(x)+str(agente_id))
					dpg.add_text(str(agente.status.value),parent=str(x)+str(agente_id),tag='status_'+str(x)+str(agente_id))
					dpg.add_text(str(agente.ip),parent=str(x)+str(agente_id))
					dpg.add_text(str(Grant[agente.Grant_level.value]),parent=str(x)+str(agente_id))
					
				dpg.add_table_cell(parent=str(x)+str(agente_id),tag='botones'+str(x)+str(agente_id))
				dpg.add_button(label='lanzar',user_data=[x,agente.id],parent='botones'+str(x)+str(agente_id),callback=lanzar)

				dpg.add_same_line(parent='botones'+str(x)+str(agente_id))
				dpg.add_button(label='parar',user_data=[x,agente.id],parent='botones'+str(x)+str(agente_id),callback=parar)
				dpg.add_same_line(parent='botones'+str(x)+str(agente_id))
				dpg.add_button(label='eliminar',user_data=[x,agente.id],parent='botones'+str(x)+str(agente_id),callback=eliminar)
	else:
		dpg.show_item('ventana_agentes')






cpu_data = []
Gpu_data = []
internet_data = []
time_data = []
RAM_data = []
for i in range(1,50):
    cpu_data.append(0)
    internet_data.append(0)
    RAM_data.append(0)
    time_data.append(i)
    Gpu_data.append(0)

# Función para obtener el porcentaje de uso de la CPU
def get_cpu_usage():
    return psutil.cpu_percent(interval=None)

# Función para manejar la actualización del gráfico en tiempo real en segundo plano
#














#probar mas adelante


def get_kbps():
    global t0, net_stats0
    t = time.time()
    net_stats = psutil.net_io_counters().bytes_recv

    elapsed_time = t - t0
    received_bytes = net_stats - net_stats0

    # Calcular la velocidad de recepción en kilobits por segundo (kbps)
    if elapsed_time > 0:
        kbps = (received_bytes * 8) / (elapsed_time * 1024)
        return kbps
    else:
        return 0


def update_plot_thread(proyecto,agent,gui, stop_event):
	global t0
	global net_stats0
	while not stop_event.is_set():
		kbps=0
		cpu_percentage=0
		ram=0
		if gui=='':
			for x in projects[proyecto].gui:
				url=str(x)+'/search/'+str(proyecto)+'/'
				respuesta = requests.get(url)
				if respuesta.status_code == 200:
					aux = respuesta.json()
					kbps=kbps+aux['kbps']
					cpu_percentage =cpu_percentage+aux['CPU']
					ram=ram+aux['RAM']
				else:
					kbps=0
					cpu_percentage =0
		else:
			if str(agent)=='todos' or str(agent)=='no hay agentes lanzados' :
				agent=''
			url=str(gui)+'/search/'+str(proyecto)+'/'+str(agent)
			respuesta = requests.get(url)
			if respuesta.status_code == 200:
				aux = respuesta.json()
				kbps=aux['kbps']
				cpu_percentage =aux['CPU']
				ram=aux['RAM']
			else:
				kbps=0
				cpu_percentage =0
				ram=0
		
        # Agregar el nuevo punto de datos a la lista
		cpu_data.append(cpu_percentage)
		internet_data.append(kbps)
		RAM_data.append(ram)
        # Limitar la longitud de los datos para evitar la sobrecarga del gráfico
		max_data_points = 50
		if len(cpu_data) > max_data_points:
			cpu_data.pop(0)
			internet_data.pop(0)
			RAM_data.pop(0)
			
		t0 = time.time()
		net_stats0 = psutil.net_io_counters().bytes_recv
		
        # Borrar el gráfico actual
		dpg.configure_item("series_tag", x=time_data, y=cpu_data)
		dpg.configure_item("aa", x=time_data, y=internet_data)
		dpg.configure_item("RAM", x=time_data, y=RAM_data)
        # Esperar 2 segundos antes de la próxima actualización
		
		
		time.sleep(2)
	print('se ha parado el hilo')



#(((Get-Counter "\GPU Engine(*engtype_3D)\Utilization Percentage").CounterSamples | Where-Object { $_.InstanceName -like "*pid_14856*" })).CookedValue

def update_plot_thread_GPU(proyecto,agent,gui, stop_event):
	global Gpu_data
	while not stop_event.is_set():
		if gui=='':
			for x in projects[proyecto].gui:
				url=str(x)+'/GPU/'+str(proyecto)+'/'
				#respuesta = requests.get(url)
				respuesta.status_code==0
				if respuesta.status_code == 200:
					aux = respuesta.json()
					GPU_percent=aux['GPU']
				else:
					GPU_percent=0
		else:
			if str(agent)=='todos':
				agent=''
			url=str(gui)+'/GPU/'+str(proyecto)+'/'+str(agent)
			#respuesta = requests.get(url)
			respuesta.status_code==0
			if respuesta.status_code == 200:
				aux = respuesta.json()
				GPU_percent=aux['GPU']
			else:
				GPU_percent=0
		
        # Agregar el nuevo punto de datos a la lista
		Gpu_data.append(GPU_percent)
        # Limitar la longitud de los datos para evitar la sobrecarga del gráfico
		max_data_points = 50
		if len(Gpu_data) > max_data_points:
			Gpu_data.pop(0)
			
        # Borrar el gráfico actual
		#dpg.configure_item("series_tag", x=time_data, y=cpu_data)
		#dpg.configure_item("aa", x=time_data, y=internet_data)
		dpg.configure_item("aaa", x=time_data, y=Gpu_data)
        # Esperar 2 segundos antes de la próxima actualización
		
		time.sleep(1)
	print('se ha parado el hilo')

















update_thread=None
update_thread_GPU=None
stop_event=None
def run(sender, app_data):
	global update_thread,stop_event,cpu_data ,Gpu_data ,internet_data,time_data,update_thread_GPU
	proyecto=dpg.get_value("proyecto")
	print(proyecto)
	print('a')
	if proyecto!='':
		agent=dpg.get_value("combo_agents")
		gui=dpg.get_value("combo_guis")
		try:
			dpg.delete_item('buttons')
		except:
			pass
		
		ventana_existe = dpg.does_item_exist("Graficos")
		print(f"¿La ventana existe? {ventana_existe}")
		if ventana_existe==False:
			dpg.add_group(parent='grupo',tag='grupo_Graficos')
			dpg.add_group(horizontal=True, parent='grupo_Graficos',height=50,tag='botones_graficos')
			with dpg.child_window( parent='grupo_Graficos',tag='Graficos'):
				with dpg.collapsing_header(label="CPU"):
					with dpg.plot(label="Consumo de CPU (%)",tracked=True, height=200):
						dpg.add_plot_axis(dpg.mvXAxis, label="Tiempo")
						dpg.set_axis_limits(dpg.last_item(), 0, 50)
						dpg.add_plot_axis(dpg.mvYAxis, label="CPU (%)", tag="y_axis")
						dpg.set_axis_limits(dpg.last_item(), 0, 100)
						dpg.add_line_series(label="CPU",parent="y_axis",tag='series_tag' , x=time_data , y= cpu_data)
				with dpg.collapsing_header(label="GPU"):
					with dpg.plot(label="Consumo de GPU (%)",tracked=True, height=200):
						dpg.add_plot_axis(dpg.mvXAxis, label="Tiempo")
						dpg.set_axis_limits(dpg.last_item(), 0, 50)
						dpg.add_plot_axis(dpg.mvYAxis, label="GPU (%)", tag="y_axis1")
						dpg.set_axis_limits(dpg.last_item(), 0, 100)
						dpg.add_line_series(label="GPU",parent="y_axis1",tag='aaa' , x=time_data , y= cpu_data)
				with dpg.collapsing_header(label="Internet"):
					with dpg.plot(label="Consumo de Internet (%)",tracked=True, height=200):
						dpg.add_plot_axis(dpg.mvXAxis, label="Tiempo")
						dpg.set_axis_limits(dpg.last_item(), 0, 50)
						dpg.add_plot_axis(dpg.mvYAxis, label="Internet", tag="y_axis2")
						dpg.set_axis_limits(dpg.last_item(), 0, 100)
						dpg.add_line_series(label="INTERNET",parent="y_axis2",tag='aa' , x=time_data , y= cpu_data)
				with dpg.collapsing_header(label="RAM"):
					with dpg.plot(label="Consumo de RAM (%)",tracked=True, height=200):
						dpg.add_plot_axis(dpg.mvXAxis, label="Tiempo")
						dpg.set_axis_limits(dpg.last_item(), 0, 50)
						dpg.add_plot_axis(dpg.mvYAxis, label="RAM(%)", tag="y_axis3")
						dpg.set_axis_limits(dpg.last_item(), 0, 100)
						dpg.add_line_series(label="RAM",parent="y_axis3",tag='RAM' , x=time_data , y= cpu_data)

# In	iciar el hilo para la actualización en segundo plano
			stop_event = threading.Event()
			update_thread = threading.Thread(target=update_plot_thread, args=(proyecto, agent, gui, stop_event))
			update_thread.start()

			update_thread_GPU = threading.Thread(target=update_plot_thread_GPU, args=(proyecto, agent, gui, stop_event))
			update_thread_GPU.start()
			dpg.add_button(label='parar graficos',parent="botones_graficos",callback=stopgraficos)
			dpg.add_button(label='nuevas Estadisticas',parent="botones_graficos",callback=run)

		else:
			stop_event.set()  # Establece la bandera para indicar que el hilo debe detenerse
			update_thread.join()
			update_thread_GPU.join()
			cpu_data = []
			Gpu_data = []
			internet_data = []
			time_data = []
			for i in range(1,50):
				cpu_data.append(0)
				internet_data.append(0)
				time_data.append(i)
				Gpu_data.append(0)

			stop_event = threading.Event()
			update_thread = threading.Thread(target=update_plot_thread, args=(proyecto, agent, gui, stop_event))
			update_thread.start()
			update_thread_GPU = threading.Thread(target=update_plot_thread_GPU, args=(proyecto, agent, gui, stop_event))
			update_thread_GPU.start()
	else:
		pass
def stopgraficos():
	stop_event.set()  # Establece la bandera para indicar que el hilo debe detenerse
	update_thread.join()
	update_thread_GPU.join()
	dpg.delete_item('grupo_Graficos')
	ventana_estadisticas()

def on_close():
		try:
			stop_event.set()  # Establece la bandera para indicar que el hilo debe detenerse
			update_thread.join()
			update_thread_GPU.join()
		except:
			pass
		with open("gui.txt", "r") as archivo:
			for linea in archivo:
				url=str(linea).replace("\n", "")+':4999'+'/Parar_agentes'
				respuesta = requests.get(url)
				if respuesta.status_code == 200:
					url=str(linea).replace("\n", "")+':4998'+'/STOP'
					respuesta = requests.get(url)
					if respuesta.status_code == 200:
						exit
					else:
						return dpg.ClosePopup
					
				else:
					return dpg.ClosePopup
				
def ventana_estadisticas():
	dpg.add_group(height=100,parent='grupo',tag='buttons')
	dpg.add_button(label='Estadisticas',parent="buttons",callback=run)
	
	
dpg.set_exit_callback(on_close)

#dpg.add_button(label='Manage',parent="botones",callback=manage)

dpg.create_viewport(title='Dashboard Skynnet', width=1200, height=500)
ventana_estadisticas()
dpg.set_primary_window('ventana',True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

