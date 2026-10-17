import socket
import threading
import sys
import io
import struct
import selectors
import collections
from Message import MESSAGE_TYPES 
from Message import MESSAGE_NAMES 
from Message import build_ActualMessage 
from Message import build_HandshakeMessage 
from Message import HANDSHAKE_LEN
from Message import parse_HandshakeMessage

sPort = 8000  # The server will be listening on this port number
tcpEstablished = changeNeighPref = changeUnchokeNeigh = unchoking = choking = receiveHave = \
    receiveInter = receiveNoInter = dwnldPiece = cmpltDwnld = False

class Server:
    @staticmethod
    def main(serverID):
        print(f"The server "+ str(serverID) +"is running on port {sPort}.")
        listener = socket.create_server(("", sPort))
        clientNum = 1
        try:
            while True:
                conn, _addr = listener.accept()
                tcpEstablished = True
                Server.Handler(conn, clientNum, serverID).start()
                #log_event()
                print(f"Client {clientNum} is connected.")
                clientNum += 1
        finally:
            listener.close()

    class Handler(threading.Thread):
        def __init__(self, connection, no, serverID):
            super().__init__()
            self.message = None           # message received from the client
            self.MESSAGE = None           # Uppercase message send to the client
            self.connection = connection
            self.in_stream = None         # Stream read from the socket ("in" is reserved in Python)
            self.out = None               # Stream write to the socket
            self.no = no                  # The index number of the client
            self.serverID = serverID
            self.clientID = None

        def run(self):
            try:
                # Initialize inputStream and outputStream
                self.out = self.connection.makefile("w", encoding="utf-8")
                self.in_stream = self.connection.makefile("r", encoding="utf-8")

                try:
                    #Whenever a connection is established between two peers, each of the peers of the 
                    #connection sends to the other one the handshake message before sending other messages. 

                    recvhsmsg = self._recv_exact(HANDSHAKE_LEN)
                    header, remote_peer_ID = parse_HandshakeMessage(recvhsmsg)
                    self.clientID= remote_peer_ID
                    print("Server's handshake message received")

                    hsmsg = build_HandshakeMessage(self.serverID)
                    self.connection.sendall(hsmsg)
                    print("Server's handshake message sent")

                    while True:
                        # Receive the message sent from the client
                        line = self.in_stream.readline()
                        if not line:
                            raise EOFError
                        self.message = line.rstrip("\n")
                        # Show the message to the user
                        print(f"Receive message: {self.message} from client {self.no}")
                        # Capitalize all letters in the message
                        self.MESSAGE = self.message.upper()
                        # Send MESSAGE back to the client
                        self.send_message(self.MESSAGE)
                except UnicodeDecodeError:
                    print("Data received in unknown format", file=sys.stderr)
            except (OSError, EOFError):
                print(f"Disconnect with Client {self.no}")
            finally:
                # Close connections
                for stream in (self.in_stream, self.out, self.connection):
                    try:
                        if stream is not None:
                            stream.close()
                    except OSError:
                        print(f"Disconnect with Client {self.no}")
                        
        #Receives 32-byte handshake message header
        def _recv_exact(self, n: int) -> bytes:
            buf = bytearray()
            while len(buf) < n:
                chunk = self.connection.recv(n - len(buf))
                if not chunk:
                    raise EOFError("Connection closed while receiving handshake")
                buf.extend(chunk)
            return bytes(buf)

        def send_message(self, msg):
            try:
                self.out.write(msg + "\n")
                self.out.flush()
                #print(f"Send message: {msg} to Client {self.no}")
            except OSError as e:
                print(f"I/O error: {e}")

if __name__ == "__main__":
    Server.main()
