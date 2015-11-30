def join_batman_network(password = 'tenticles',
			interface = 'wlan2',
			network_name = 'batmesh', 
			ap_mac = '02:12:34:56:78:9A',
			gw_ip = '192.168.2.4', 
			channel = '1'):
	'''Create a BATMAN network using Raspbian.

	ARGS:
	@network_name		-- The name of the network you would like to create
	@ap_mac				-- The MAC address to assign the Access Point
	@channel			-- The channel number to join (STRING or INT)

	RETURN:
	None
	'''
	import time
	from batman_setup import load_batman
	from run_command import run_command

	load_batman.load_batman(password)

	run_command('sudo /etc/init.d/network-manager stop', password)

	# Configure wlan0 to have a Maximum Transmission Unit to 1532 frames
	# This is standard for BATMAN-Advanced. Most protocols only require
	# 1500 frames, but BATMAN-Advanced uses the spare 32 frames to append
	# its header.
	run_command('sudo ifconfig ' + interface + ' mtu 1532', password)

	# Configure wlan0 with the specifications given.
	run_command('sudo ifconfig ' + interface + ' down && ' +
		    'sudo iwconfig ' + interface + ' mode ad-hoc essid ' 
		    + network_name + ' ap ' + ap_mac + ' channel ' + 
 		    str(channel), password)

	# Add wlan0 to the list of BATMAN-Advanced available interfaces, then
	# start wlan0 and the corresponding BATMAN-Advanced interface.
	run_command('sudo batctl if add ' + interface, password)
	run_command('sudo ifconfig ' + interface + ' up', password)
	run_command('sudo ifconfig bat0 up', password)
	run_command('sudo ifconfig bat0 192.168.2.15', password)
	run_command('sudo route add default gw ' + gw_ip, password)
	run_command('sudo batctl gw_mode client', password)

	with open('/etc/resolv.conf', 'rt') as f:
		text = f.read()
		if text.find('nameserver 8.8.8.8') == -1:
			text = text + '\nnameserver 8.8.8.8\n'
		if text.find('nameserver 8.8.4.4') == -1:
			text = text + 'nameserver 8.8.4.4\n'
		with open('/tmp/etc_resolv.tmp', 'wt') as temp:
			temp.write(text)

	run_command('sudo mv /tmp/etc_resolv.tmp /etc/resolv.conf')

if __name__ == '__main__':
	join_batman_network('tenticles')

