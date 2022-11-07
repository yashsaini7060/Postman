import socket
import sys
import os
from dataclasses import dataclass
from datetime import datetime
import time

PERSONAL_ID = '09665A'
PERSONAL_SECRET = '4c1ad1b77651992faa6e31e7f3cbdb8b' 
IP = 'localhost'
FORMAT = "ascii"
SIZE = 1024
PORT=0
SEND_PATH=''
def get_port_and_path():
    global PORT
    global SEND_PATH
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
            if x.lower().startswith("send_path"): 
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
        
        # dir_list = os.listdir(send_path)
        # dir_list.sort()
        # print(dir_list)

        PORT=server_port
        SEND_PATH=send_path
        print(SEND_PATH)






def setup_client_connection() -> socket.socket:
    """
    Sets up a client socket connection to the server for communication over a network. If 
    the client cannot connect, after 20 seconds, the program automatically exits with an error.
    Returns:
        A client socket connected to the server.
    """
    global PORT
    global IP
    
    get_port_and_path()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allows us to relaunch the application quickly without having to worry about "address already 
    # in use errors"
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Sets timeout of socket: we will use this to check if we can connect to the server
    sock.settimeout(20)

    try:
        # Connct to server
        
        sock.connect((IP,PORT))
    except:
        print("C: Cannot establish connection")
        sys.exit(3)
        

    return sock

def check_status_code(client_sock: socket.socket, expected_status_code: int) -> None:
    """
    Checks the status code obtained by the server in response to a message. If the server's status 
    code does not match the expected provided code, a ValueError is raised.
    Args:
        client_sock: the client socket connected to the server.
        expected_status_code: the status code we expect to receive from the server after sending a 
            message.
    Raises:
        ValueError: if the status code returned by the server does not match expected_status_code.
    """
    # Get response from server
    global FORMAT
    server_data = client_sock.recv(SIZE)
    server_data_str = server_data.decode(FORMAT)

    #printing string
    out_str="S: " + server_data_str[:-1]
    print(out_str, flush=True)

    # Split response from server into list (on whitespace)
    server_data_ls = server_data_str.split()

    # Get the status code from the server response list
    actual_status_code = int(server_data_ls[0])

    if actual_status_code != expected_status_code:
        raise ValueError(f"expected code {expected_status_code}, but was {actual_status_code}")
    


def send_helo(client_sock: socket.socket) -> None:
    """
    Sends a HELO SMTP message to the mail server.
    Args:
        client_sock: the client socket connected to the USYD mail server.
    """
    string="EHLO 127.0.0.1\r\n"
    client_sock.send(string.encode(FORMAT))
    string= 'C: ' + string[:-1]
    print(string, flush=True)


def send_mail(client_sock, path):

    print(path)
    try:
        f = open(path, "r")
        lines = f.readlines()
        print(lines)
    except:
        print('unable to open file')
    
    # global SEND_PATH

    # dir_list = os.listdir(SEND_PATH)
    # dir_list.sort()
    # print(dir_list)




def main():

    client_sock = setup_client_connection()
    
    with client_sock:
        #Session Initiation
        check_status_code(client_sock, 220)
        send_helo(client_sock)
        check_status_code(client_sock, 250)
        check_status_code(client_sock, 250)
        
        
        print(SEND_PATH)
        f = open(SEND_PATH, "r")
        lines = f.readlines()
        print(lines)
        # dir_list = os.listdir(SEND_PATH)
        # dir_list.sort()
        # print(dir_list)
        # i=0
        # while i<len(dir_list):
        #     file_name=dir_list[i]
        #     path=SEND_PATH+'\\'+file_name
        #     print(file_name)
        #     send_mail(client_sock, path)
        #     i=i+1
        
 


if __name__ == "__main__":
    main() 