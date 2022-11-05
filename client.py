import socket
import sys
import os
from dataclasses import dataclass
from datetime import datetime


PERSONAL_ID = '09665A'
PERSONAL_SECRET = '4c1ad1b77651992faa6e31e7f3cbdb8b' 



@dataclass(frozen=True)
class EmailUser:
    """
    A dataclass containing information about an email sender/recipient.
    """
    name: str
    """The full name of the email sender/recipient."""

    address: str
    """The email address of the email sender/recipient."""


@dataclass(frozen=True)
class Email:
    """
    A dataclass containing all necessary information to send a plaint text email.
    """
    from_user: EmailUser
    """The sender of the email."""

    recipients: tuple[EmailUser, ...]
    """All recipients of the email."""

    subject: str
    """The subject of the email (which may be empty)."""

    body: str
    """The body of the email as a string."""




def get_configs():
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
        
        return client_port, inbox_path

    except:
        exit(1)

def get_email_body() -> str:
    """
    Gets the content of the email body.
    Returns:
        The content of the email body as a string.
    """
    print("Enter email contents below (press Ctrl+D to finish):")
    content = sys.stdin.read()

    return content


def get_to_users() -> tuple[EmailUser, ...]:
    """
    Gets all recipients that the email will be sent to.
    Returns:
        A tuple containing all recipients the email will be addressed to.
    """
    to_users = []
    input_finished = False
    while not input_finished:
        to_name = input("Enter a recipient name: ")
        to_addr = input("Enter this recipients address: ")
        to_user = EmailUser(to_name, to_addr)
        to_users.append(to_user)

        input_users_confirmation = input("Would you like to input any more recipients? [y/N] ").lower()
        if input_users_confirmation == "y":
            continue
        else:
            input_finished = True
        
        print()
    
    print(f"{len(to_users)} total recipients entered")
    return tuple(to_users)


def get_from_user() -> EmailUser:
    """
    Gets information about the user sending the email.
    Returns:
        An EmailUser representing the user sending the email.
    """
    from_name = input("Enter the from name: ")
    from_addr = input("Enter the first part of the from address (i.e. the <name> in "
                      "<name>@it.usyd.edu.au): ") + "@it.usyd.edu.au"
    from_user = EmailUser(from_name, from_addr)
    return from_user


def get_email_data() -> Email:
    """
    Gets all necessary information required to send an email via the USYD mail server via SMTP.
    Returns:
        An Email object containing all necessary information for a plain text email.
    """
    from_user = get_from_user()
    to_users = get_to_users()
    subject = input("Enter subject (press 'Enter' for no subject): ")
    content = get_email_body()

    email = Email(from_user, to_users, subject, content)
    return email






def setup_client_connection() -> socket.socket:
    """
    Sets up a client socket connection to the USYD mail server for communication over a network. If 
    the client cannot connect, after 20 seconds, the program automatically exits with an error.
    Returns:
        A client socket connected to the USYD mail server.
    """

    PORT, INBOX_PATH = get_configs()
    IP = "localhost"
    SMTP_SERVER = (IP, PORT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allows us to relaunch the application quickly without having to worry about "address already 
    # in use errors"
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Sets timeout of socket: we will use this to check if we can connect to the server
    sock.settimeout(20)

    try:
        # Connct to server
        sock.connect(SMTP_SERVER)
    except TimeoutError:
        sys.exit("Error: cannot connect to USYD SMTP server.\n"
                 "Are you on the USYD Network, or connected to the USYD VPN?")

    return sock

def check_status_code(client_sock: socket.socket, expected_status_code: int) -> None:
    """
    Checks the status code obtained by the server in response to a message. If the server's status 
    code does not match the expected provided code, a ValueError is raised.
    Args:
        client_sock: the client socket connected to the USYD mail server.
        expected_status_code: the status code we expect to receive from the server after sending a 
            message.
    Raises:
        ValueError: if the status code returned by the server does not match expected_status_code.
    """
    # Get response from server
    server_data = client_sock.recv(256)
    server_data_str = server_data.decode()
    # Split response from server into list (on whitespace)
    server_data_ls = server_data_str.split()

    # Get the status code from the server response list
    actual_status_code = int(server_data_ls[0])

    if actual_status_code != expected_status_code:
        raise ValueError(f"expected code {expected_status_code}, but was {actual_status_code}")


def send_data(client_socket: socket.socket, email: Email) -> None:
    """
    Sends the DATA message to the mail server, as well as the MIME data portion of the email.
    Args:
        client_socket: the client socket connected to the USYD mail server.
        email: the Email object containing all necessary information for a plain text email.
    """
    client_socket.send(b"DATA\r\n")
    check_status_code(client_socket, 354)

    mime_version = "MIME-Version: 1.0\r\n"

    date = datetime.now().astimezone()
    date_str = date.strftime("Date: %a, %-d %b %Y %X %z\r\n")

    from_header = f"From: {email.from_user.name} <{email.from_user.address}>\r\n"

    to_users_str = [f"{recipient.name} <{recipient.address}>" for recipient in email.recipients]
    to_header = "To: " + ", ".join(to_users_str) + "\r\n"

    subject = f"Subject: {email.subject}\r\n"

    content_type = "Content-Type: text/plaintext;\r\n"

    client_socket.send(mime_version.encode())
    client_socket.send(date_str.encode())
    client_socket.send(from_header.encode())
    client_socket.send(to_header.encode())
    client_socket.send(subject.encode())
    client_socket.send(content_type.encode())
    client_socket.send(b"\r\n")
    client_socket.send(email.body.encode() + b"\r\n")

    client_socket.send(b".\r\n")
    check_status_code(client_socket, 250)


def send_to_recipients(client_socket: socket.socket, email: Email) -> None:
    """
    Send a RCPT TO messager to the mail server for all recipients
    Args:
        client_socket: the client socket connected to the USYD mail server.
        email: the Email object containing all necessary information for a plain text email.
    """
    for recipient in email.recipients:
        rcpt_to = f"RCPT TO:<{recipient.address}>\r\n"
        client_socket.send(rcpt_to.encode())
        check_status_code(client_socket, 250)


def send_helo(client_sock: socket.socket) -> None:
    """
    Sends a HELO SMTP message to the mail server.
    Args:
        client_sock: the client socket connected to the USYD mail server.
    """
    client_sock.send(b"HELO python.client\r\n")


def send_email_via_server(client_sock: socket.socket, email: Email) -> None:
    """
    Communicates with the USYD mail server in order to send an email using the SMTP protocol.
    Args:
        client_sock: the client socket connected to the USYD mail server.
        email: the Email object containing all necessary information for a plain text email.
    """
    with client_sock:
        # Check initial status code after connection (220)
        check_status_code(client_sock, 220)
        print
        # Send the HELO message, and check the status code
        # send_helo(client_sock)
        # check_status_code(client_sock, 250)

        # Send the MAIL FROM message to the server, and check the status code
        from_user = email.from_user
        mail_from = f"MAIL FROM:<{from_user}>\r\n"
        client_sock.send(mail_from.encode())
        # check_status_code(client_sock, 250)

        # Send the RCPT TO headers for all recipients
        send_to_recipients(client_sock, email)

        # Send DATA, and email data to server
        send_data(client_sock, email)

        # Quit server gracefully by sending QUIT
        client_sock.send(b"QUIT\r\n")

        # Printed if no exceptions occur
        print("Email sent successfully!")





def main():
    # print("S: 220 Service ready", flush=True)
    client_sock = setup_client_connection()
    with client_sock:
        check_status_code(client_sock, 220)
        print("S: 220 Service ready", flush=True)
    # email = get_email_data()
    # send_email_via_server(client_sock, email)
 


if __name__ == "__main__":
    main() 