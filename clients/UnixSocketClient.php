<?php
class UnixSocketClient {
	private $socketAddress;
	private $socketTimeOut;
	private $maxDownloadSize = 2048;
	private $socketClient;

	public function __construct( $socketAddress ){
		$this->setSocketAddress( $socketAddress );
		$this->socketTimeOut = 10;
	}

	public function setSocketAddress( $socketAddress ){
		$this->socketAddress = 'unix://' . $socketAddress;
		$this->socketClient = false;
	}

	public function sendData($data){
		if(!$this->_hasConnection()){
			if(!$this->_openConnection())
				return false;
		} else {
			if(feof($this->socketClient)){
				if(!$this->_openConnection())
					return false;
			}
		}

		$this->_sendDataSize( $data );
		$this->_sendData( $data );
		return $this->_getResponse();
	}

	private function _hasConnection(){
		if($this->socketClient)
			return true;
		return false;
	}

	private function _openConnection(){
		echo "open connection\n";
		$this->socketClient = stream_socket_client(
							$this->socketAddress, 
							$errno, 
							$errstr, 
							$this->socketTimeOut
						);

		if(!$this->socketClient)
			return false;
		return true;
	}

	private function _sendDataSize( $data ){
		$dataSize = pack('V', strlen($data));
		fwrite($this->socketClient,  $dataSize);
	}

	private function _sendData( $data ){
		fwrite($this->socketClient,  $data);
	}

	private function _getResponse(){
		$size = $this->_getResponseSize();

		if($size < 0)
			return false;

		$current_size = 0;
		$buff = '';

		while ($current_size < $size){
			$dowload_size = $size - $current_size;
			if ($dowload_size > $this->maxDownloadSize)
				$dowload_size = $this->maxDownloadSize;

			$data = fread($this->socketClient, $dowload_size);

			if(empty($data))
				break;

			if (strlen($data) + $current_size > $size)
				$data = substr($data, 0, $size-$current_size);
			
			$buff .= $data;
			$current_size += strlen($data);
		}
		return $buff;
	}

	private function _getResponseSize(){
		$size = fread($this->socketClient, 4);
		$size = unpack('V', $size);
		
		if(isset($size[1]))
			return $size[1];
		else
			return -1;
	}

	public function close(){
		if($this->socketClient && !feof($this->socketClient)){
			fclose($this->socketClient);
			$this->socketClient = null;
		}
	}

}