def join_batman_network(network_name = 'squids_network', 
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

	load_batman.load_batman()

	# Configure wlan0 to have a Maximum Transmission Unit to 1532 frames
	# This is standard for BATMAN-Advanced. Most protocols only require
	# 1500 frames, but BATMAN-Advanced uses the spare 32 frames to append
	# its header.
	run_command('sudo ifconfig wlan0 mtu 1532')

	# Configure wlan0 with the specifications given.
	run_command('sudo ifconfig wlan0 down && sudo iwconfig wlan0 mode ad-hoc ' +
				'essid ' + network_name + ' ap ' + ap_mac + ' channel ' + str(channel))

	# Add wlan0 to the list of BATMAN-Advanced available interfaces, then
	# start wlan0 and the corresponding BATMAN-Advanced interface.
	run_command('sudo batctl if add wlan0')
	run_command('sudo ifconfig wlan0 up')
	run_command('sudo ifconfig bat0 up')
	run_command('sudo route add default gw ' + gw_ip)
	run_command('sudo batctl gw_mode client')


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', 'network', default = 'squids_network')
	parser.add_argument('-a', 'ap_mac', default = '02:12:34:56:78:9A')
	parser.add_argument('-c', 'channel', default = '1')
	args = parser.parse_args()

	join_batman_network(args.network, args.ap_mac, args.channel)

