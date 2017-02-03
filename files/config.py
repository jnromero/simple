#!/usr/bin/python

def setConfig(location):
	config={}

	config['packageFolder']="/steep/"
	config['currentExperiment']="/simple/"
	config['screenServerPort']=15374
	config['location']=location

	if location=="myComputer":
		config['webServerRoot']="/Users/myUsername/experiments/"
		config['serverType']="regularExperiment"	
		config['serverPort']=2345
		config['webSocketPort']=3456
		ip="localhost"
		config["domain"]="http://"+ip+":"+str(config['serverPort'])
		config["websocketURL"]="ws://"+ip+":"+str(config['webSocketPort'])
		config["screenServer"]="http://"+ip+":"+str(config['screenServerPort'])
	# elif location=="labComputer":
	# 	config['webServerRoot']="/Users/labAdmin/myUsername/experiments/"
	# 	config['serverType']="regularExperiment"	
	# 	config['serverPort']=4567
	# 	config['webSocketPort']=5678
	# 	ip="12.345.67.89"
	# 	config["domain"]="http://"+ip+":"+str(config['serverPort'])
	# 	config["websocketURL"]="ws://"+ip+":"+str(config['webSocketPort'])
	# 	config["screenServer"]="http://"+ip+":"+str(config['screenServerPort'])
	return config