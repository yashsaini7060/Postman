import socket
import sys
import os

# PERSONAL_ID = '09665A'
# PERSONAL_SECRET = '4c1ad1b77651992faa6e31e7f3cbdb8b' 

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
        if os.access(inbox_path, os.W_OK):
            return server_port, inbox_path
        else:
            exit(2)
    except:
        exit(1)




def main():
    PORT, INBOX_PATH = get_port_and_path()
    IP = socket.gethostbyname(socket.gethostname())
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = "utf-8"

    # print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    # print("[LISTENING] Server is listening.")
    print("S: 220 Service ready")
    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        """ Receiving the filename from the client. """
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the filename.")
        file = open(filename, "w")
        conn.send("Filename received.".encode(FORMAT))

        """ Receiving the file data from the client. """
        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the file data.")
        file.write(data)
        conn.send("File data received".encode(FORMAT))

        """ Closing the file. """
        file.close()

        """ Closing the connection from the client. """
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()