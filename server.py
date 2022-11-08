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
    if client_response.endswith('\n'):
            client_response=client_response[:-1]
    client_response = "C: " + client_response
    print(client_response, flush=True)
    return client_response





def check_status_code(conn, expected_status_code: str) -> None:

    # Get response from server
    global FORMAT
    global SIZE
    client_response= conn.recv(SIZE).decode(FORMAT)

    if client_response=='':
        print("C: Connection lost", flush=True)
        exit(3)

    if client_response.endswith('\n'):
            client_response=client_response[:-1]
    out_str = "C: " + client_response
    print(out_str, flush=True)

    client_response = client_response.split()
    actual_status_code = client_response[0].lower()

    if(expected_status_code==""):
        pass
    else:  
        if actual_status_code != expected_status_code.lower():
            raise ValueError(f"expected code {expected_status_code}, but was {actual_status_code}")
    

    
def send_response(conn , res):
    res=res.split(" ")
    res=res[0]
    print(res)
    if(res=="MAIL"):
        pass
        
    # data=0
    # return data

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
        check_status_code(conn, "EHLO")
        send_data(conn, "250 127.0.0.1\r\n")
        # send_response(conn)
        check_status_code(conn, "MAIL")
        send_data(conn, "250 Requested mail action okay completed\r\n")
        check_status_code(conn, "RCPT")
        send_data(conn, "250 Requested mail action okay completed\r\n")
        check_status_code(conn, "RCPT")
        send_data(conn, "250 Requested mail action okay completed\r\n")
        check_status_code(conn, "DATA")
        send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
        check_status_code(conn, "")
        send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
        check_status_code(conn, "")
        send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
        check_status_code(conn, "")
        send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
        check_status_code(conn, "")
        send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")



        """ Closing the connection from the client. """
        conn.close()
        # print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main() 