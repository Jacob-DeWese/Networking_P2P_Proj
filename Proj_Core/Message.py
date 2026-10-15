import struct

MESSAGE_TYPES = {
    "CHOKE": 0,
    "UNCHOKE": 1,
    "INTERESTED": 2,
    "NOT_INTERESTED": 3,
    "HAVE": 4,
    "BITFIELD": 5,
    "REQUEST": 6,
    "PIECE": 7
}

MESSAGE_NAMES = {
    0: "CHOKE",
    1: "UNCHOKE",
    2: "INTERESTED",
    3: "NOT_INTERESTED",
    4: "HAVE",
    5: "BITFIELD",
    6: "REQUEST",
    7: "PIECE"
}

#need to figure out how to calculate the size for BITFIELD and pieces.
MESSAGE_PAYLOADSIZE = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 4,
    5: 10,
    6: 4,
    7: 10
}

HANDSHAKE_LEN = 32

#needs to figure out how to build the data of payload
#Maybe a converstion (JPG to Bytefile) 
def build_Payload() -> bytes:
    payloadBytes = bytes(5);
    return payloadBytes

#Haven't implemented the payload yet. Need actual data of payload.
def build_ActualMessage(msgLength, msgType, payload=b""):
    lengthBytes = msgLength.to_bytes(4, 'big');
    typeBytes = msgLength.to_bytes(1, 'big');

    return (lengthBytes + typeBytes + payload)

    # handshake message is 32 bytes.
def build_HandshakeMessage(peer_ID):
    #18 bytes
    headerBytes = b"P2PFILESHARINGPROJ";
    #10-byte zero bits
    zeroBytes = bytes(10);
    peerIDBytes = peer_ID.to_bytes(4, 'big');
    return (headerBytes + zeroBytes + peerIDBytes)

#Parses the received handshake message
def parse_HandshakeMessage(data: bytes):
    if len(data) != 32:
        raise ValueError("There are {len(data)} bytes in the handshake, not 32.")
    headerBytes = data[0:18];
    zeroBytes = data[18:28];
    peer_ID = struct.unpack(">I", data[28:32])[0]

    #Data Validation
    if headerBytes !=  b"P2PFILESHARINGPROJ":
        raise ValueError(f"Handshake header is wrong: {headerBytes!r}")
    if zeroBytes != bytes(10):
        raise ValueError("Handshake zero bits are not 10-byte zero bits")
    return headerBytes, peer_ID
    
'''
    def parse_message():
        length = recv(4)
        type = recv(1)
        payload = recv(length-1)
'''

'''
File purpose:
Used by PeerProcess.py
'''
