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
EHOL=False
AUTH=False
FILEDATA=[]




def get_port_and_path():
    global PORT
    global INBOX_PATH
    config_file=''
    try:
        config_file=sys.argv[1]
    except:
        exit(1)
    if config_file!='':
        config_file=sys.argv[1]

        # FILE READINGG
        f = open(config_file,"r")
        lines = f.readlines()
        # print(lines)
        if len(lines)<2:
            exit(2)

        # SERVER PORT
        server_port=''

        for x in lines:
            if x.lower().startswith("server_port"): 
                server_port=x
        
        if server_port!='':
            server_port = server_port.split('=')
            server_port=server_port[1]
            if server_port.endswith('\n'):
                server_port=int(server_port[:-1])
            if server_port < 1024:
                exit(2)
        else:
            exit(2)

        # SEND PATH
        send_path=''

        for x in lines:
            if x.lower().startswith("inbox_path"): 
                x = x.split("=")
                x=x[1]
                if x.endswith('\n'):
                    x=x[:-1]
                send_path=x
        if send_path!='':
            if os.access(send_path, os.R_OK):
                pass
        else:
            exit(2)
        
        PORT=server_port
        INBOX_PATH=send_path



def send_response(conn , string):
    global FORMAT
    conn.send(string.encode(FORMAT))
    if string.endswith('\n'):
            string=string[:-1]
    new_str="S: " + string
    print(new_str, flush=True)
    

def get_response(conn):

    client_response= conn.recv(SIZE).decode(FORMAT)
    if not client_response:
        print("S: Connection lost", flush=True)
        return
    else:
        if client_response.endswith('\n'):
            client_response=client_response[:-1]
        out_str = "C: " + client_response
        print(out_str, flush=True)

        client_code=client_response.split(" ")

        return client_code[0], client_response






def check_status_code(conn, expected_status_code: str) -> None:

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
    

    


def setup_client_connection():
    global PORT
    global IP
    
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    """ Bind the IP and PORT to the server. """

    server.bind((IP, PORT))

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen(1)


    conn, addr = server.accept()

    return conn





def auto_res(conn,prev_data):
    global EHOL
    global AUTH
    global FILEDATA

    code, response=get_response(conn)


    if response.lower()=="quit\r":
        send_response(conn,'221 Service closing transmission channel\r\n')
    elif response.lower()=="noop\r":
        send_response(conn,'250 Requested mail action okay completed\r\n')
    elif prev_data=="service ready":
        if response.lower()=="ehlo 127.0.0.1\r":
            send_response(conn,'250 127.0.0.1\r\n')
            EHOL=True
            send_response(conn,'250 AUTH CRAM-MD5\r\n')
            auto_res(conn,'AUTH CRAM-MD5')
        else:
            send_response(conn,'501 Syntax error in parameters or arguments\r\n')
            auto_res(conn,'service ready')
        

        




def main():
    get_port_and_path()
    conn = setup_client_connection()

    send_response(conn, "220 Service ready\r\n")
    auto_res(conn,'service ready')
    # check_status_code(conn, "EHLO")
    # send_data(conn, "250 127.0.0.1\r\n")
    # # send_response(conn)
    # check_status_code(conn, "MAIL")
    # send_data(conn, "250 Requested mail action okay completed\r\n")
    # check_status_code(conn, "RCPT")
    # send_data(conn, "250 Requested mail action okay completed\r\n")
    # check_status_code(conn, "RCPT")
    # send_data(conn, "250 Requested mail action okay completed\r\n")
    # check_status_code(conn, "DATA")
    # print("dataaaaaaaaa")
    # send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
    # check_status_code(conn, "")
    # send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
    # check_status_code(conn, "")
    # send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
    # check_status_code(conn, "")
    # send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")
    # check_status_code(conn, "")
    # send_data(conn, "354 Start mail input and <CRLF>.<CRLF>\r\n")



    """ Closing the connection from the client. """
    conn.close()
    # print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main() 