import socket
import sys

class Client:
    def __init__(self,host="localhost",port=7234):
        self.host = host
        self.port = port
        self.requestSocket = None  # Socket connect to server
        self.out = None            # Stream write to the socket
        self.in_stream = None      # Stream read from the socket
        self.message = ""          # Message send to the server
        self.MESSAGE = ""          # Capitalized message read from the server

    def run(self):
        try:
            # Create a socket to connect to the server
            self.requestSocket = socket.create_connection((self.host, self.port))
            print(f"Connected to {self.host} in port {self.port}")

            # Initialize inputStream and outputStream
            self.out = self.requestSocket.makefile("w", encoding="utf-8")
            self.in_stream = self.requestSocket.makefile("r", encoding="utf-8")

            while True:
                # Read a sentence from the standard input
                self.message = input("Hello, please input a sentence: ")
                # Send the sentence to the server
                self.send_message(self.message)
                # Receive the upperCase sentence from the server
                self.MESSAGE = self.in_stream.readline()
                if not self.MESSAGE:
                    print("Server closed the connection")
                    break
                # Show the message to the user
                print("Receive message: " + self.MESSAGE)

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

    # Send a message to the output stream
    def send_message(self,message):
        try:
            # Stream write the message
            self.out.write(message + "\n")
            self.out.flush()
        except OSError as e:
            print(f"I/O error: {e}", file=sys.stderr)


# Main method
if __name__ == "__main__":
    client = Client()
    client.run()
"""
IMPORTANT TO IMPLEMENT
Whenever the TCP connection is made to another peer, generate the log -->
[Time]: Peer [peer_ID 1] makes a connection to Peer [peer_ID 2]
- Time = hour:minute:second
- peer_ID 1 = client
- peer_ID 2 = server

Whenever the peer changes its preferred neighbors, it generates the following log -->
[Time]: Peer [peer_ID] has the preferred neighbors [preferred neighbor ID list]
- [preferred neighbor list] = list of peer IDs separated by comma ','

Whenever a peer changes its optimistically unchoked neighbor, it generates the following log -->
[Time]: Peer [peer_ID] has the optimistically unchoked neighbor [optimistically unchoked neighbor ID]

Whenever a peer is unchoked by a neighbor (when a peer receives an unchoking message), it generates the log -->
[Time]: Peer [peer_ID 1] is unchoked by [peer_ID 2]
- [peer_ID 1] = unchoked
- [peer_ID 2] = peer who unchokes

... (not writing them all out, but point is Client implements the log)
"""