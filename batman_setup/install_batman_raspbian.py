




def install_batman_raspbian(path = '/squids_tmp'):
	'''Download BATMAN-Advanced package, unpack it, install it, and load it.

	ARGS:
	@path -- The absolute path of where the BATMAN-Advanced module will be built.
			If the path specified does not exist it will be created.
			Default path is /squids_tmp

	RETURN:
	None
	'''
	import os
	import sys
	sys.path.append('..')
	from download_batman import download_batman
	from load_batman import load_batman
	from run_command import run_command

	# Check if @path does not exist create it then download BATMAN to it
	if not os.path.exists(path):
		os.mkdir(path)
	download_batman(path)

	# Run a chain of linux operations to install BATMAN and its dependencies
	run_command('sudo apt-get update')
	run_command("sudo apt-get install linux-headers-'*'")
	run_command('sudo apt-get install g++ gcc')
	run_command('cd ' + batpath[: -7] + '/; make')
	out, err = run_command('cd ' + batpath[: -7] + '/; uname -r')
	run_command('sudo apt-get install aptitude')
	run_command('sudo aptitude qt4-dev-tools')
	run_command('sudo apt-get install libncurses5-dev libncursesw5-dev')
	run_command('cd /usr/src/linux-headers-' + out + '/; sudo make xconfig; sudo make menuconfig; sudo make oldconfig;')
	
	# Attempt to load BATMAN and print success
	if load_batman():
		print '\033[1;43m' + 'BATMAN-Advanced' + '\033[1;m' + ' was successfully loaded\n'
	else:
		print 'Could not load BATMAN-Advanced\n'

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('path', default = '/squids_tmp')

	args = parser.parse_args()

	install_batman_raspbian(args.path)