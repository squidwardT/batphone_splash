def install_batctl():
	'''Installs batctl a BATMAN-Advanced configuration tool.

	ARGS:
	None

	RETURN:
	None
	'''
	import sys
	sys.path.append('..')
	from run_command import run_command	
	run_command('sudo apt-get batctl')

if __name__ == '__main__':
	install_batctl()