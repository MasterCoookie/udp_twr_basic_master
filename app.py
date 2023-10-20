import socket
import time
import random

class Initiator:
    def __init__(self, ip, port, uwb_address):
        self.ip = ip
        self.port = port
        self.uwb_address = uwb_address

        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sckt.bind(('0.0.0.0', 12))

    def send(self, message):
        self.sckt.sendto(message.encode(), (self.ip, self.port))

    def receive(self):
        try:
            data = self.sckt.recv(1024)
            print(data.decode())
        except socket.timeout:
            print("Timeout Occured.")
        self.sckt.close()



if __name__ == "__main__":
    tag_a = Initiator("192.168.0.112", 7, "DD")
    # tag_b = Initiator("192.168.0.113", 7, "EE")
    anchors = ("AA", "BB")
    for i in range(1):
        time.sleep(0.1)
        anchor = random.choice(anchors)
        tag_a.send(anchor)
        tag_a.receive()
        # time.sleep(0.1)
        # anchor = random.choice(anchors)
        # tag_b.send(anchor)