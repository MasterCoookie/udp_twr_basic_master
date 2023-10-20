import socket
import time
import random

class Initiator:
    def __init__(self, ip, port, uwb_address):
        self.ip = ip
        self.port = port
        self.uwb_address = uwb_address

class UDPSocket:
    def __init__(self):
        self.bound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bound_socket.bind(('0.0.0.0', 12))
        self.bound_socket.settimeout(1)

    def send(self, message, ip, port):
        self.bound_socket.sendto(message.encode(), (ip, port))

    def receive(self):
        try:
            data = self.bound_socket.recv(1024)
            print(data.decode())
        except socket.timeout:
            print("Timeout Occured.")



if __name__ == "__main__":
    tag_a = Initiator("192.168.0.112", 7, "DD")
    tag_b = Initiator("192.168.0.113", 7, "EE")
    anchors = ("AA", "BB")
    sckt = UDPSocket()
    for i in range(10):
        time.sleep(0.5)
        anchor = random.choice(anchors)

        print(f'Sending from {tag_a.uwb_address} to {anchor}')
        sckt.send(anchor, tag_a.ip, tag_a.port)
        sckt.receive()
        sckt.receive()

        time.sleep(0.5)
        anchor = random.choice(anchors)

        print(f'Sending from {tag_b.uwb_address} to {anchor}')
        sckt.send(anchor, tag_b.ip, tag_b.port)
        sckt.receive()
        sckt.receive()
    
    sckt.bound_socket.close()