from socket import socket, AF_UNIX, SOCK_STREAM
from .SocketStreamHandler import SocketStreamHandler

class SocketClient:
	
	def __init__(self, socketAddress):
		self._socketAddress = socketAddress
		self._conn = None

	def sendData(self, data):
		handler = SocketStreamHandler(self.getConnnection())
		handler.sendData(data)
		return handler.getData()

	def getConnnection(self):
		if self._conn != None:
			return self._conn

		self._conn = socket(AF_UNIX, SOCK_STREAM)

		try:
			self._conn.connect(self._socketAddress)
		except Exception as msg:
			raise Exception("Error with connecting: " + msg.strerror)

		return self._conn
		

	def close(self):
		self._conn.close()
