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
        self.results_buffer = [[] for _ in range(dvices_no)]

    def send(self, message, ip, port, verbose=False):
        if verbose:
            print(f'Sending {message} to {ip}:{port}')
        self.bound_socket.sendto(message.encode(), (ip, port))

    def receive(self, result_prefix, device_index, verbose=False):
        try:
            data = self.bound_socket.recv(1024)
            if verbose:
                print(f'{result_prefix} received {data.decode()}')
            self.results_buffer[device_index].append(f'{result_prefix} received {data.decode()}')
            
        except socket.timeout:
            if verbose:
                print(f'{result_prefix} timeout')
            self.results_buffer[device_index].append(f'{result_prefix} timeout')

    def dump_results(self, file_prefix):
        for i, results in enumerate(self.results_buffer):
            with open(f'{file_prefix}_{i}.txt', 'w') as f:
                for result in results:
                    f.write(f'{result.strip()}\n')



if __name__ == "__main__":
    anchors = ("AA", "BB")
    tags = (Initiator("192.168.0.112", 7, "DD"), Initiator("192.168.0.113", 12, "EE"))
    sckt = UDPSharedSocket(12, len(tags))

    start = time.time()

    for exchange_index in range(100):
        for i, tag in enumerate(tags):
            anchor = random.choice(anchors)
            sckt.send(anchor, tag.ip, tag.port, True)
            sckt.receive(f'#{exchange_index}. {tag.uwb_address} to {anchor}', i, True)
            sckt.receive(f'#{exchange_index}. {tag.uwb_address} to {anchor}', i, True)
    
    end = time.time() - start
    sckt.bound_socket.close()
    sckt.dump_results('results')
    
    print(f'Time elapsed: {end}')