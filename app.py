import socket
import time
import random

class Initiator:
    def __init__(self, ip, port, uwb_address):
        self.ip = ip
        self.port = port
        self.uwb_address = uwb_address

class UDPSocket:
    def __init__(self, port):
        self.port = port
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
    for i in range(10):
        time.sleep(0.1)
        anchor = random.choice(anchors)

        tag_a.bind_sckt()
        tag_a.send(anchor)
        tag_a.receive()
        tag_a.receive()
        tag_a.sckt.close()

        time.sleep(0.1)

        anchor = random.choice(anchors)
        tag_b.bind_sckt()
        tag_b.send(anchor)
        tag_b.receive()
        tag_b.receive()
        tag_b.sckt.close()