import socket
import tqdm
import os
import argparse
import requests
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

parser = argparse.ArgumentParser(description='Input name you want to set')
parser.add_argument('name',
                  help='name to send to',)
args = parser.parse_args()

s = socket.socket()

r = requests.post(f"http://{SERVER_HOST}:5000/api/{args.name}")

s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
client_socket, address = s.accept()
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
with client_socket:
    while True:
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for _ in progress:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
