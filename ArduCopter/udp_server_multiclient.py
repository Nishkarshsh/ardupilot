import socket
import threading
import time
import udp_server
from datetime import datetime
class UDPServerMultiClient(udp_server.UDPServer):
    ''' A simple UDP Server for handling multiple clients '''

    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket_lock = threading.Lock()

    def handle_request(self, data, client_address):
        ''' Handle the client '''

        # handle request
        name = data.decode('utf-8')
        resp = self.get_latitude(name)
        self.printwt("[ REQUEST from {client_address} ]")
        print('\n', name, '\n')

        # send response to the client
        self.printwt("[ RESPONSE to {client_address} ]")
        with self.socket_lock:
            self.sock.sendto(resp.encode('utf-8'), client_address)
        print('\n', resp, '\n')

    def configure_server(self):


        ''' Configure the server '''
        # create UDP socket with IPv4 addressing

        self.printwt('Creating socket...')
        self.printwt('Socket created')
        # bind server to the address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.printwt('Binding server to {self.host}:{self.port}...')
        self.printwt('Server binded to {self.host}:{self.port}')

    def wait_for_client(self):
        ''' Wait for clients and handle their requests '''

        try:
            while True: # keep alive

                try: # receive request from client
                    data, client_address = self.sock.recvfrom(4096)

                    c_thread = threading.Thread(target = self.handle_request,
                                            args = (data, client_address))
                    c_thread.daemon = True
                    c_thread.start()

                except OSError as err:
                    self.printwt(err)

        except KeyboardInterrupt:
            self.shutdown_server()

def main():
    ''' Create a UDP Server and handle multiple clients simultaneously '''

    try:
        while(True):

            udp_server_multi_client = UDPServerMultiClient('127.0.0.1', 10000)
            udp_server_multi_client.configure_server()
            udp_server_multi_client.wait_for_client()

    except KeyboardInterrupt:
        self.shutdown_server()

if __name__ == '__main__':
    main()