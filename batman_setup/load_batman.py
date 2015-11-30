def load_batman(password):
	'''Load BATMAN-Advanced.

	ARGS:
	None

	RETURN:
	Boolean	-- True if successful; otherwise False
	'''
	import sys
	sys.path.append('..')
	from run_command import run_command

	# Run the load and store stdout
	run_command('sudo modprobe batman-adv', password)
	out, err = run_command('dmesg', password)

	# Check if load was successful
	if 'BATMAN-Advanced was loaded successfully' in out:
		return True
	return False

if __name__ == '__main__':
	load_batman()
