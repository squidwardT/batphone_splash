from datetime import datetime

from flask import (
	Flask,
	abort,
	flash,
	redirect,
	render_template,
	request,
	url_for,
)
from flask.ext.stormpath import (
	StormpathError,
	StormpathManager,
	User,
	login_required,
	login_user,
	logout_user,
	user,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nananananananana'
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey-YVVIY4R3LM986736KU1OS4LNX.properties'
app.config['STORMPATH_APPLICATION'] = 'batman_splash'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

stormpath_manager = StormpathManager(app)

@app.route('/')
def show_index():
	import netifaces
	interfaces = [interface for interface in netifaces.interfaces() if interface.find('wlan') != -1]
	return render_template('index.html', option_list=interfaces)

@app.route('/error')
def show_error():
	return render_template('error.html')

@app.route('/join', methods=['POST'])
def join():
	import requests
	import webbrowser
	from sockets import TCPSocket
	from run_command import run_command
	from read_mac_address import read_mac_address
	from join_batman_network import join_batman_network

	error = None
	try:
		from 
		from run_command import run_command
		from sockets import TCPSocket
		from join_batman_network import join_batman_network
		ssid = request.form['ssid']
		publickey = request.form['publickey']
		mac = request.form['mac']
		password = request.form['admin_password']
		interface = request.form['interfaces']

		join_batman_network(password = password,
				    interface = interface,
				    network_name = ssid,
				    ap_mac = mac)

		if_mac = read_mac_address(interface)
		sock = TCPSocket()
		sock.connect('192.168.2.15', 5005)
		sock.write('DHCP ' + if_mac + '/n')

		response = socket.read()
		run_command('sudo ifconfig bat0 ' + response, password)		
		
		print 'Successfully Joined Network'
	except StormpathError, err:
		error = err.message
	
	try:
		server_address = 'http://batphone.co/'
		print 'Attempting Request On ' + server_address
		response = requests.get(server_address)
		if response.status_code != 200:
			raise requests.exceptions.ConnectionError
		print 'Server Accessible. Loading Page....'
		webbrowser.open(server_address)
	except requests.exceptions.RequestException:
		try:
			print 'Failed to Connect to Server'
			lan_host_address = 'http://192.168.2.8:3000/'
			print 'Attempting Request on ' + lan_host_address
			response = requests.get(lan_host_address)
			if response.status_code != 200:
				raise requests.exceptions.ConnectionError
			print 'LAN Host Accessible. Loading Page....'
			webbrowser.open(lan_host_address)
		except requests.exceptions.RequestException:
			return render_template('error.html', error = error)
	return 'OK'			
			

def start_app():
	app.run(debug = True, use_reloader = False)

if __name__=='__main__':
	app.run()
