import Client
import Server
import threading
import time

class PeerProcess():
    def __init__(self):
        self.server_thread = [];
        self.client_thread = [];
        #A list of servers listed in PeerInfo.cfg Need peerInfo reader!
        #peer0= dict(peer_ID =1001, host="192.168.1.131", port=8000)
        #peer1= dict(peer_ID =1002, host="192.168.1.139", port=8000)
        peer0= dict(peer_ID =1001, host="10.138.187.221", port=8000)

        #A list of dicts stores peers info.
        self.peerInfo = [peer0]

    def startClient(self):

        while True:
            addrLocalhost = input("Please enter the remote host (IP or localhost): ").strip()
            portNum = input("Please enter the remote port: ").strip()

            if not addrLocalhost:
                print("Host cannot be empty. Try again.")
                continue

            try:
                port = int(portNum)
                if not (1 <= port <= 65535):
                    raise ValueError("Port out of range")
            except ValueError:
                print("Port out of range.")
                continue

            try:
                self.myClient = Client.Client(addrLocalhost, port)  
                print(f"Client created for {addrLocalhost}:{port}")
                self.myClient.run();
                break;
            except Exception as e:
                print(f"Failed client: {e}")
                break

    def startServer(self):
        try:
            server = Server.Server()
            myServer = threading.Thread(
                target=server.main,
                daemon=True
            )
            myServer.start()              
            print("Server started in background thread.")
            self.server_thread.append(myServer)
        except Exception as e:
            print(f"Failed to start server: {e}")


    def run(self):
        """Start both server and client."""
        print("Starting PeerProcess...")
        self.startServer()   
        self.startClient()   

        #keep the main thread alive
        if self.server_thread is not None:
            self.server_thread.join()
    
def main():
    print("main is called")
    myPeerProcess = PeerProcess();
    myPeerProcess.run()
    
if __name__ == "__main__":
    main()       

"""
File purpose:


Thinking through (for reading PeerInfo.cfg):
1) PeerProcess gets the information that is within PeerInfo.cfg
2) It then runs Client, loading the [listening port] of the peer into client
3) If a failure occurs, output message, disregard for now (peer could still be in-network)
4) If a success occurs, output success message
    - PeerProcess becomes either the core file that calls others to run, or just offloads role to
    next file in process. Regardless, step 5:
5) Establish handshake connection
"""

