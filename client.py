import socket
import sys
import os

PERSONAL_ID = '09665A'
PERSONAL_SECRET = '4c1ad1b77651992faa6e31e7f3cbdb8b' 



def get_port_and_path():
    try:
        config_file=sys.argv[1]
        f = open(config_file,"r")
        lines = f.readlines()
        server_port=lines[0]
        x = server_port.split("=")
        server_port=x[1]
        server_port=int(server_port)
        inbox_path=lines[2]
        x = inbox_path.split("~")
        inbox_path=x[1]
        if inbox_path.endswith("\n"):
            inbox_path=inbox_path[:-1]
            inbox_path=inbox_path[1:]
        if os.access(inbox_path, os.R_OK):
            return server_port, inbox_path
        else:
            exit(2)
    except:
        exit(1)




def main():
    PORT, INBOX_PATH = get_port_and_path()
    IP = socket.gethostbyname(socket.gethostname())
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 1024

    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)
    rv=client.recv(SIZE).decode(FORMAT)
    print(rv)
    
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