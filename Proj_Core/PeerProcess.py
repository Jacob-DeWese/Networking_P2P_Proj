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

