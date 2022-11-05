import socket
import sys
import os

# PERSONAL_ID = '09665A'
# PERSONAL_SECRET = '4c1ad1b77651992faa6e31e7f3cbdb8b' 

IP = "127.0.0.1"

def get_port_and_path():
    try:
        config_file=sys.argv[1]

        # FILE READINGG
        f = open(config_file,"r")
        lines = f.readlines()
        if(len(lines)<5):
            exit(2)


        # SERVER PORT

        server_port=lines[0]
        if server_port.lower().startswith("send_path"):
            x = server_port.split("=")
            server_port=x[1]
            server_port=int(server_port)
            
            if server_port < 1024:
                exit(2)

        # CLIENT PORT

        client_port=lines[1]
        if client_port.lower().startswith("client_port"):
            x = client_port.split("=")
            client_port=x[1]
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
        if send_path.startswith("~/"):
            send_path=send_path[2:]
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
        if spy_path.startswith("~/"):
            spy_path=spy_path[2:]
        if os.access(spy_path, os.W_OK):
            pass
        else:
            exit(2)
        
        return server_port, inbox_path

    except:
        exit(1)

# def get_port_and_path():
#     try:
#         config_file=sys.argv[1]
#         f = open(config_file,"r")
#         lines = f.readlines()
#         server_port=lines[0]
#         x = server_port.split("=")
#         server_port=x[1]
#         server_port=int(server_port)
#         inbox_path=lines[2]
#         x = inbox_path.split("~")
#         inbox_path=x[1]
#         if inbox_path.endswith("\n"):
#             inbox_path=inbox_path[:-1]
#             inbox_path=inbox_path[1:]
#         if os.access(inbox_path, os.W_OK):
#             return server_port, inbox_path
#         else:
#             exit(2)
#     except:
#         exit(1)




def main():
    PORT, INBOX_PATH = get_port_and_path()

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

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        conn.send("220 Service ready".encode(FORMAT))


        """ Receiving the hello  from the client. """
        hello = conn.recv(SIZE).decode(FORMAT)
        print(hello)
        ehol
        conn.send("250 Service ready".encode(FORMAT))
        mail_from = conn.recv(SIZE).decode(FORMAT)
        print(mail_from)
        conn.send("250 Service ready".encode(FORMAT))
        send_to_recipient = conn.recv(SIZE).decode(FORMAT)
        print(send_to_recipient)
        conn.send("250 Service ready".encode(FORMAT))
        send_data = conn.recv(SIZE).decode(FORMAT)
        print(send_data)
        conn.send("250 Service ready".encode(FORMAT))


        """ Closing the connection from the client. """
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()