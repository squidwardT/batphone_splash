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
app.config['DEBUG'] = True
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

	error = None
	try:
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
	except StormpathError, err:
		error = err.message
	
	try:
		server_address = 'http://batphone.co/'
		response = requests.get(server_address)
		webbrowser.open(server_address)
	except requests.exception.ConnectionError:
		try:
			lan_host_address = 'http://192.168.2.8:3000/'
			response = requests.get(lan_host_address)
			webbrowser.open(lan_host_address)
		except requests.exception.ConnectionError:
			return render_template('error.html', error = error)
	return 'OK'			
			

def start_app():
	app.run()

if __name__=='__main__':
	app.run()
