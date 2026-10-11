import Client
import Server
class PeerProcess:
    def __init__(self):
        self.myClient = None
        self.myServer = None
        self.server_thread = None

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
        self.myServer = Server.Server()   
        self.myServer.main();

        ''''
        try:
            
            self.myServer = Server.Server()   
            self.server_thread = threading.Thread(
                target=self.myServer.start,  
                daemon=True
            )
            self.server_thread.run()
            print("Server started in background thread.")
        except Exception as e:
            print(f"Failed to start server: {e}")
        '''

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
