import socket
import time
import random

class Initiator:
    def __init__(self, ip, port, uwb_address):
        self.ip = ip
        self.port = port
        self.uwb_address = uwb_address

    def send(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(message.encode())
        s.close()



if __name__ == "__main__":
    tag_a = Initiator("192.168.0.112", 7, "DD")
    tag_b = Initiator("192.168.0.113", 7, "EE")
    anchors = ("AA", "BB")
    while 1:
        