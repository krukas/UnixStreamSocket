Unix Stream Socket  
=====================

Simple python module for creating an unix stream server and client for sending an arbitrary length of data.

Flow of the program, you run the server as a deamon application. Client send a data reqeust wich can be a simple "hello world" string or JSON string. The server handles the data en gives back a response. The response message can also be arbitrary length of data.

**Max data size**
Before the data is send from the client to the server or server to client. A 4 bytes stream is send containing the data size that is going to be send. 4 bytes => 32 bits => 2147483647 bytes (2Gb) is the theoretical max data transfer size. 

###Example Server
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
    
    >>> Hello World

###Client
    from unixstreamsocket import SocketClient
    
    client = SocketClient('/tmp/python_unix_socket_steam.sock')
    response = client.sendData("Hello World")
    print(response)
    
    >>> okey...

##Other clients
At the moment there is only a PHP client, that is also the reason why I created this python module. I needed a way to send data to a python deamon from an PHP page.

###PHP client
    
    require_once 'UnixSocketClient.php';
    $socketClient = new UnixSocketClient('/tmp/python_unix_socket_steam.sock');
    echo $socketClient->sendData("Hello World");
    
    >>> okey...

##Wish list

 - Keeping track of all the ServerThreads, for crasfully closing running threats on shutdown and for closing threads that exceeds the to by set max connection time.

