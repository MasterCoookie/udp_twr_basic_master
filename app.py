import socket
import time
import random

class Initiator:
    def __init__(self, ip, port, uwb_address):
        self.ip = ip
        self.port = port
        self.uwb_address = uwb_address

    def send(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', 12))
        s.sendto(message.encode(), (self.ip, self.port))
        try:
            data = s.recv(1024)
            print(data.decode())
        except socket.error:
            print("Error Occured.")
        except socket.timeout:
            print("Timeout Occured.")
        s.close()



if __name__ == "__main__":
    tag_a = Initiator("192.168.0.112", 7, "DD")
    tag_b = Initiator("192.168.0.113", 7, "EE")
    anchors = ("AA", "BB")
    for i in range(100):
        anchor = random.choice(anchors)
        tag_a.send(anchor)
        # print
        anchor = random.choice(anchors)
        tag_b.send(anchor)