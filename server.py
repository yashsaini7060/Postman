import socket
import sys
import os

# PERSONAL_ID = '09665A'
# PERSONAL_SECRET = '4c1ad1b77651992faa6e31e7f3cbdb8b' 
IP = 'localhost'
FORMAT = "ascii"
SIZE = 1024
PORT=0
INBOX_PATH=''
def get_port_and_path():
    global PORT
    global INBOX_PATH
    try:
        config_file=sys.argv[1]

        # FILE READINGG
        f = open(config_file,"r")
        lines = f.readlines()
        if(len(lines)<5):
            exit(2)


        # SERVER PORT

        server_port=lines[0]
        if server_port.lower().startswith("server_port"):
            x = server_port.split("=")
            server_port=x[1]
            if server_port.endswith("\n"):
                server_port=server_port[:-1]
            server_port=int(server_port)
            
            if server_port < 1024:
                exit(2)

        # CLIENT PORT

        client_port=lines[1]
        if client_port.lower().startswith("client_port"):
            x = client_port.split("=")
            client_port=x[1]
            if client_port.endswith("\n"):
                client_port=client_port[:-1]
            client_port=int(client_port)

            if client_port < 1024 and server_port==client_port:
                exit(2)

        
        # INBOX PATH
        inbox_path=lines[2]
        
        if inbox_path.lower().startswith("inbox_path"):
            x = inbox_path.split("=")
            inbox_path=x[1]
            if inbox_path.endswith("\n"):
                inbox_path=inbox_path[:-1]
            if inbox_path.startswith("~/"):
                inbox_path=inbox_path[2:]
            if os.access(inbox_path, os.W_OK):
                pass
            else:
                exit(2)

        # SEND PATH
        send_path=lines[3]
        if send_path.lower().startswith("send_path"):
            x = send_path.split("=")
            send_path=x[1]
        if send_path.endswith("\n"):
            send_path=send_path[:-1]
        if os.access(send_path, os.R_OK):
            pass
        else:
            exit(2)
        
        # SPY PATH

        spy_path=lines[4]
        if spy_path.lower().startswith("spy_path"):
            x = spy_path.split("=")
            spy_path=x[1]
        if spy_path.endswith("\n"):
            spy_path=spy_path[:-1]
        if os.access(spy_path, os.W_OK):
            pass
        else:
            exit(2)
        # print(server_port)
        # return server_port, inbox_path
        PORT=server_port
        INBOX_PATH=inbox_path
    except:
        exit(1)


def send_data(conn , string):
    global FORMAT
    conn.send(string.encode(FORMAT))
    if string.endswith('\n'):
            string=string[:-1]
    new_str="S: " + string
    print(new_str, flush=True)
    

def get_response(conn):
    client_response= conn.recv(SIZE).decode(FORMAT)
    return client_response

def log_client(response):
    if response.endswith('\n'):
            response=response[:-1]
    response = "C: " + response
    print(response, flush=True)
    


def main():
    global PORT
    global IP
    get_port_and_path()

    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """

    server.bind((IP, PORT))

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen(1)

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()

        # Service redy messagess
        send_data(conn, "220 Service ready\r\n")
        ehol_response = get_response(conn)
        log_client(ehol_response)
        if ehol_response=="EHLO 127.0.0.1\r\n":
            send_data(conn, "250 127.0.0.1\r\n")
            send_data(conn, "250 AUTH CRAM-MD5\r\n")



        """ Closing the connection from the client. """
        conn.close()
        # print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main() 