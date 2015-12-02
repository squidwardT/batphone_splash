import shlex
import select
import socket
from threading import Thread
from TCPSocket import TCPSocket


class TCPServerSocket(TCPSocket):

    '''CLASS: Representing a BATMAN-Advanced node as a server socket listening on
                      a port to take action or pass data

    FIELDS:
    @self.sock 	-- The child socket this socket has been built from.
    @self.clients	-- The list of clients that are communicating with this
                                   device in some way.
    '''

    def __init__(self, address, port):
        '''CONSTRUCTOR: Run parent constructor and initialize the clients array
        '''
        super(TCPServerSocket, self).__init__(address)
        self.clients = []
        self.address = address
       	self.port = port

    def start_server(self, interpreter = None):
        '''Listen on a @port for incoming application connections. When connected to
        store the client's information and attempt to read its transmitted data.

        ARGS:
        @port		-- The port number to start the server socket on

        RETURN:
        None		-- Theoretically Endless
        '''

        # Bind this socket to port and listen for connections
        self.sock.bind((self.address, self.port))
        self.sock.listen(5)

        # While the application is running attempt listen for connections and read the
        # connecting devices message.
        while True:
            # Get the connected socket and make a Batman Socket out of it
            client, address = self.sock.accept()
            tcp_client = TCPSocket(address, client)

            # Start threads to add devices to the list of clients and read
            # their messages
            read_thread = Thread(
                target=self.read_client, args=[tcp_client, interpreter])
            read_thread.start()

    def read_client(self, clients):
        '''Receive the client's message.

        ARGS:
        @clients		-- The client socket to be read from.
        @address		-- IGNORE. Purely for error prevention

        RETURNS:
        @args 			-- A list of arguments to be interpreted
        '''
	import shlex
        msg = clients.read()
	args = shlex.split(msg)

        if args[0] == 'DHCP':
		# NEED TO WRITE
		ip = find_open_ip(args[1])
		clients.sendall(ip)
	else:
		print 'Invalid Request ' + msg

if __name__ == '__main__':
    server = TCPServerSocket('whatever')
    server.start_server()
