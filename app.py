import socket
import time
import random

class Initiator:
    def __init__(self, ip, port, uwb_address, sckt):
        self.ip = ip
        self.port = port
        self.uwb_address = uwb_address
        self.sckt = sckt

class UDPSocket:
    def __init__(self, out_port):
        self.bound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bound_socket.bind(('0.0.0.0', out_port))
        self.bound_socket.settimeout(1)
        # open file
        self.file = open(f'data_{out_port}.txt', "w+")

    def send(self, message, ip, port):
        self.bound_socket.sendto(message.encode(), (ip, port))

    def receive(self, uwb_address):
        try:
            data = self.bound_socket.recv(1024)
            # print(data.decode())
            self.file.write(f'{uwb_address}: {data.decode()}')
        except socket.timeout:
            self.file.write(f'{uwb_address}: Timeout\n')



if __name__ == "__main__":
    anchors = ("AA", "BB")
    freq = 50
    delay = 1/(freq/2)

    tag_a = Initiator("192.168.0.13", 13, "DD", UDPSocket(13))
    tag_b = Initiator("192.168.0.112", 12, "EE", UDPSocket(12))
    start = time.time()
    for i in range(100):
        # time.sleep(1/freq)
        anchor = random.choice(anchors)

        print(f'Sending from {tag_a.uwb_address} to {anchor}')
        tag_a.sckt.send(anchor, tag_a.ip, tag_a.port)
        tag_a.sckt.receive(tag_a.uwb_address)
        tag_a.sckt.receive(tag_a.uwb_address)

        # time.sleep(delay)
        anchor = random.choice(anchors)

        print(f'Sending from {tag_b.uwb_address} to {anchor}')
        tag_b.sckt.send(anchor, tag_b.ip, tag_b.port)
        tag_b.sckt.receive(tag_b.uwb_address)
        tag_b.sckt.receive(tag_b.uwb_address)
    
    end = time.time() - start
    print(f'Time elapsed: {end}')
    tag_a.sckt.bound_socket.close()
    tag_b.sckt.bound_socket.close()