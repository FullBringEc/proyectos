import subprocess
import os

# Creamos los descriptores de archivos como dos vulgares archivos
# con permisos de escritura llamados 'archivo_out' y 'archivo_err'
def ejecutar(comando):
	dirname = os.path.dirname(__file__)
	#subprocess.check_call(['ls'], cwd=wd)
	#subprocess.call('cd '+, shell=True)
	#subprocess.Popen(['cd', '/home' ])
	return(str(os.system('java -jar "C:\Program Files\ComprobantesElectronicosOffline\ComprobantesDesktop.jar"'))+' hecho')
	'''process = subprocess.Popen(comando.split(), stdout=subprocess.PIPE, cwd = dirname)
	out, err = process.communicate()
	if err != None:
		return str(err)
	else:
		return str(out)
	'''

	#os.path.abspath('../../'))
	#return 'cd ' + os.path.dirname(__file__)
	#return	os.path.dirname(os.path.abspath(__file__))
	#
	
