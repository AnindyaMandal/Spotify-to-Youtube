import socket
import re
import os


def get_codestate():
    # Define socket host and port
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 8888

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.settimeout(5.0)
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    while True:
        try:
            # Wait for client connections
            client_connection, client_address = server_socket.accept()

            # Get the client request
            request = client_connection.recv(1024).decode()
            blocks = request.split("\n")
            get_statement = blocks[0]
            print(type(get_statement))
            print(get_statement)

            code = re.search(r'(?<=code=).*?(?=&state=)',
                             get_statement).group()
            print(len(code))
            state = re.search(r'(?<=&state=).*?(?= HTTP/)',
                              get_statement).group()
            print(len(state))

            # Send HTTP response
            response = 'HTTP/1.0 200 OK\n\nCode: ' + code + '\nState: ' + state
            client_connection.sendall(response.encode())
            client_connection.close()

            if (len(code) == 264 and len(state) == 16):
                os.environ['SPOTIFY_CODE'] = code
                os.environ['SPOTIFY_STATE'] = state
                server_socket.close()
                print("Server closed!")
                break

        except KeyboardInterrupt:
            print("KB Interrupt!")
            server_socket.close()
            break
        except TimeoutError:
            print("Timed Out!")
            break
