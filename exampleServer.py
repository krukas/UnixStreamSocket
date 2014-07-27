from unixstreamsocket import SocketServer

class UnixServer(SocketServer):
	def __init__(self):
		SocketServer.__init__(self, '/tmp/python_unix_socket_steam.sock')

	def run(self, data, thread):
		#do somthing with data
		print(data)
		
		#return response
		return "okey..."

server = UnixServer()
server.start()