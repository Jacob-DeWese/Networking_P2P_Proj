import socket
import sys
import Server
from Message import MESSAGE_TYPES
from Message import MESSAGE_NAMES
from Message import build_ActualMessage
from Message import build_HandshakeMessage
from Message import HANDSHAKE_LEN
from Message import parse_HandshakeMessage
from Logger import log_event

class Client:
    def __init__(self, host="10.138.245.53", port=8000, peer_ID=1002):
        self.host = host
        self.port = port
        self.requestSocket = None  # Socket connect to server
        self.out = None  # Stream write to the socket
        self.in_stream = None  # Stream read from the socket
        self.message = ""  # Message send to the server
        self.MESSAGE = ""  # Capitalized message read from the server
        self.peer_ID = peer_ID

    def run(self):
        try:
            # Create a socket to connect to the server
            self.requestSocket = socket.create_connection((self.host, self.port))
            print(f"Connected to {self.host} in port {self.port}")

            # Whenever a connection is established between two peers, each of the peers of the
            # connection sends to the other one the handshake message before sending other messages.
            hsmsg = build_HandshakeMessage(self.peer_ID)
            self.requestSocket.sendall(hsmsg)
            print("Client handshake sent")

            recvhsmsg = self._recv_exact(HANDSHAKE_LEN)
            header, remote_peer_ID = parse_HandshakeMessage(recvhsmsg)
            print("Client handshake message received")
            with Server.logLock:
                Server.selfPeerID = self.peer_ID
                Server.connToPeer = remote_peer_ID
                Server.tcpEstablished = True
                log_event()
                Server.tcpEstablished = False
                Server.connToPeer = None

            # Initialize inputStream and outputStream
            self.out = self.requestSocket.makefile("w", encoding="utf-8")
            self.in_stream = self.requestSocket.makefile("r", encoding="utf-8")

            while True:
                # Read a sentence from the standard input
                self.message = input("Hello, please input a sentence: \n")

                # Send the sentence to the server
                self.send_message(self.message)
                # Receive the upperCase sentence from the server
                self.MESSAGE = self.in_stream.readline()
                if not self.MESSAGE:
                    print("Server closed the connection")
                    break
                # Show the message to the user
                # print("Receive message: " + self.MESSAGE)

        except ConnectionRefusedError:
            print("Connection refused. You need to initiate a server first.", file=sys.stderr)
        except socket.gaierror:
            print("You are trying to connect to an unknown host.", file=sys.stderr)
        except (EOFError, KeyboardInterrupt):
            print()
        except OSError as e:
            print(f"I/O error: {e}", file=sys.stderr)
        finally:
            # Close connection
            for stream in (self.in_stream, self.out, self.requestSocket):
                try:
                    if stream is not None:
                        stream.close()
                except OSError as e:
                    print(f"I/O error: {e}", file=sys.stderr)

    # Send a text message to the output stream
    '''
    def send_message(self,message):
        try:
            # Stream write the message
            self.out.write(message + "\n")
            self.out.flush()
        except OSError as e:
            print(f"I/O error: {e}", file=sys.stderr)
    '''

    # Receives 32-byte handshake message header
    def _recv_exact(self, n: int) -> bytes:
        buf = bytearray()
        while len(buf) < n:
            chunk = self.requestSocket.recv(n - len(buf))
            if not chunk:
                raise EOFError("Connection closed while receiving data")
            buf.extend(chunk)
        return bytes(buf)

    # Send a byte message to the output stream
    def send_message(self, message):
        try:
            if isinstance(message, str):
                message = (message + "\n").encode("utf-8")
            self.requestSocket.sendall(message)
            print(f"Client sent message: {message} to server {self.host}")

        except OSError as e:
            print(f"I/O error: {e}", file=sys.stderr)


# Main method
'''
if __name__ == "__main__":
    client = Client()
    client.run()
'''
