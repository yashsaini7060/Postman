import socket
import sys


PERSONAL_ID = '09665A'
PERSONAL_SECRET = '4c1ad1b77651992faa6e31e7f3cbdb8b' 




def main():

    config_file=sys.argv[1]
    f = open(config_file,"r")
    lines = f.readlines()
    server_port=lines[0]
    x = server_port.split("=")
    server_port=x[1]
    server_port=int(server_port)
    PORT=server_port
    IP = socket.gethostbyname(socket.gethostname())
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 1024

    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)

    """ Opening and reading the file data. """
    file = open("data/examplemail.txt", "r")
    data = file.read()

    """ Sending the filename to the server. """
    client.send("examplemail.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the file data to the server. """
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Closing the file. """
    file.close()

    """ Closing the connection from the server. """
    client.close()


if __name__ == "__main__":
    main()