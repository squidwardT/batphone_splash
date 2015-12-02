import socket
from time import sleep

class TCPSocket(object):
	'''Represents the most basic TCP socket for our application.

	ARGS:
	@address		-- The IP address of the socket
	@sock 			-- A pre-made socket that can be provided as the base
					   socket of this class. If this value is NONE, the
					   class will create a socket instead.
	'''

	def __init__(self, address, sock = None):
		self.address = address
		
		if sock is None:
			self.create_socket()
		else:
			self.sock = sock

	def create_socket(self):
		'''Create a new base socket for this class.

		ARGS:
		None

		RETURNS:
		None
		'''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, host, port):
		'''Connect the base socket to the @host provided if the application is
		listening on @port.

		ARGS:
		@host 		-- The IPv4 address of the host. STRING
		@port 		-- The port the host application is listening on. INT

		RETURNS:
		None
		'''	
		self.sock.connect((host, port))

	def write(self, message):
		'''Write a message to the host the base socket is connected to.

		ARGS:
		@message 	-- The message to be sent to the receiving device

		RETURNS:
		None
		'''

		# Write until the message is completely sent. If the pipe gets broken
		# raise a Runtime Error.
		total = 0
		while total < len(message):
			sent = self.sock.send(message[total:])
			if sent == 0:
				raise RuntimeError('Connection Broken')
			total = total + sent

	def read(self):
		'''Read a message passed from another device to the base socket.

		ARGS:
		None

		RETURNS:
		@message 	-- The message received from the currently connected
					   socket.
		'''

		# Read from the connected socket until the packet length is reached or
		# the maximum size is reached. When the entire message is recovered
		# string it together and return it. If at any point nothing is received
		# it is assumed that the connection was broken or the transmission
		# finished and what is in the buffer will be returned.
		chunks = []
		total_recieved = 0
		while total_recieved < 2048:
			chunk = self.sock.recv(min(2048 - total_recieved, 2048))
			if chunk == '':
				break
				raise RuntimeError('Connection Broken')
			chunks.append(chunk)
			total_recieved = total_recieved + len(chunk)
		return ''.join(chunks)	

	def close(self):
		self.sock.close()

if __name__ == '__main__':
	socket = TCPSocket('hello')
	socket.connect('104.131.44.2', 3000)
	socket.write('GET / HTTP/1.1\rHost: www.batphone.co\r\n\r\n')
	sleep(2)
	response = socket.read()
	print response
