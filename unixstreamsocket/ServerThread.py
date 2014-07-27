from threading 	import Thread
from .SocketStreamHandler import SocketStreamHandler

class ServerThread(Thread):
	
	def __init__(self, conn, server):
		Thread.__init__(self)
		self.conn 	= conn
		self.server = server
		self.stop 	= False

	def run(self):
		handler = SocketStreamHandler(self.conn)

		while not self.stop:
			try:
				data = handler.getData()
				response = self.server.run(data, self)
				handler.sendData(response)
			except Exception as msg:
				break

		self.conn.close()
