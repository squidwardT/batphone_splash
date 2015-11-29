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
	return render_template('index.html')

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
		join_batman_network(network_name = ssid,
				     ap_mac = mac)
	except StormpathError, err:
		error = err.message
	
	server_address = 'http://batphone.co/'
	response = request.get(server_address)
	if response.status_code == 200:
		webbrowser.open(server_address)
	else:
		lan_host_address = 'http://192.168.2.1:3000/'
		response = request.get(lan_host_address)
		if response.status_code == 200:
			webbrowser.open(lan_host_address)
		else:
			return render_template('error.html', error = error)

def start_app():
	app.run()

if __name__=='__main__':
	app.run()
