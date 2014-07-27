from os.path 	import exists
from os 		import remove, chmod
from sys		import exit
from socket 	import socket, AF_UNIX, SOCK_STREAM
from .ServerThread import ServerThread

class SocketServer:

	def __init__(self, socketAddress, max_connections=5):
		self._socketAddress = socketAddress
		self._max_connections = max_connections

	def start(self):
		# Remove old socket file if exists
		if exists( self._socketAddress ):
			remove( self._socketAddress )

		server = socket(AF_UNIX, SOCK_STREAM)

		try:
			server.bind( self._socketAddress )
			chmod(self._socketAddress, 666)
		except socket.error as msg:
			raise Exception('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
  		
		server.listen(self._max_connections)

		while True:
			conn, addr = server.accept()
			ServerThread(conn, self).start()

	def run(self, data, thread):
		"""You should override this method when you subclass Server."""


