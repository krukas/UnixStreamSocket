from socket	import error

class SocketStreamHandler:

	def __init__(self, socket):
		self._socket = socket
		self._maxDownloadSize = 2048

	def getData(self):
		try:
			size = self._getDataSize()
		except Exception as msg:
			return False
		
		current_size = 0
		buff = b""

		while current_size < size:
			dowload_size = size - current_size
			if dowload_size > self._maxDownloadSize:
				dowload_size = self._maxDownloadSize
			
			try:
				data = self._socket.recv(dowload_size)
			except error as msg:
				return False

			if not data:
				break

			if len(data) + current_size > size:
				data = data[:size-current_size]
			buff += data
		
			current_size += len(data)
		return buff.decode('utf-8')

	def _getDataSize(self):
		try:
			size = self._socket.recv(4)
		except Exception as msg:
			raise Exception("Error getting data size: "+ msg.strerror)
		return self._bytesToInt( size )	

	def sendData(self, data):
		self._sendDataSize(data)
		try:
			self._socket.send( data.encode('utf-8'))
		except Exception as msg:
			raise Exception("Error with sending data: " + msg.strerror)

	def _sendDataSize(self, data):
		try:
			size = self._intToBytes(len(data))
			self._socket.send(size)
		except Exception as msg:
			raise Exception("Error with sending data size: " + msg.strerror)

	def _bytesToInt(self, bytes):
		res = 0
		if len(bytes) != 4:
			return -1
		for i in range(4):
			res += bytes[i] << (i*8)
		return res

	def _intToBytes(self, number):
		result = bytearray()
		result.append(number & 255)
		for i in range(3):
			number = number >> 8
			result.append(number & 255)
		return result