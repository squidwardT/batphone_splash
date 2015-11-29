import argparse
from shlex import split
from subprocess import Popen, PIPE

def run_command(command):
    '''Run a terminal command.

    ARGS:
    @command	-- The terminal command to be run as a STRING.

    RETURN:
    out		-- The string written to stdout during the commands run cycle.
    err		-- The string written to stderr during the commands run cycle.
    '''

    # Split the command string into an array of terminal arguments
    args = split(command)

    # Run the command and write stdout and stderr to subprocess.PIPE
    process = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)

    # Kill the process and read and return stdout and stderr
    out, err = process.communicate()
    return out, err

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()

    run_command(args.command)
