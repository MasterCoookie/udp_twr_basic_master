import socket
import time
import random

class Initiator:
    def __init__(self, ip, port, uwb_address):
        self.ip = ip
        self.port = port
        self.uwb_address = uwb_address

class UDPSharedSocket:
    def __init__(self, out_port, dvices_no):
        self.bound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bound_socket.bind(('0.0.0.0', out_port))
        self.bound_socket.settimeout(1)
        self.results_buffer = [[]] * dvices_no

    def send(self, message, ip, port, verbose=False):
        if verbose:
            print(f'Sending {message} to {ip}:{port}')
        self.bound_socket.sendto(message.encode(), (ip, port))

    def receive(self, result_pre, device_index, verbose=False):
        try:
            data = self.bound_socket.recv(1024)
            if verbose:
                print(f'{result_pre} received {data.decode()}')
            self.results_buffer[device_index].append(f'{result_pre} received {data.decode()}')
            
        except socket.timeout:
            if verbose:
                print(f'{result_pre} timeout')
            self.results_buffer[device_index].append(f'{result_pre} timeout')



if __name__ == "__main__":
    anchors = ("AA", "BB")

    # tag_a = Initiator("192.168.0.112", 7, "DD", UDPSocket(12))
    # tag_b = Initiator("192.168.0.113", 7, "EE", UDPSocket(1547))
    tags = (Initiator("192.168.0.112", 7, "DD"), Initiator("192.168.0.113", 12, "EE"))
    sckt = UDPSharedSocket(12, len(tags))
    start = time.time()
    for exchange_index in range(100):
        for i, tag in enumerate(tags):
            anchor = random.choice(anchors)
            sckt.send(anchor, tag.ip, tag.port, True)
            sckt.receive(f'#{exchange_index}. {tag.uwb_address} to {anchor}', i, True)
            sckt.receive(f'#{exchange_index}. {tag.uwb_address} to {anchor}', i, True)
    
    sckt.bound_socket.close()
    
    end = time.time() - start
    print(f'Time elapsed: {end}')