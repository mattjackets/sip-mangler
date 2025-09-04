# Insert a custom header into SIP traffic, specifically the SIP INVITE message.

import socket

# Local ip/port to listen on
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5060

# Remote (SIP) server ip/port
TARGET_SIP_IP = "172.16.0.0"  # Replace with actual SIP server IP
TARGET_SIP_PORT = 5060

# Header to be inserted into INVITE message
X_FOO_HEADER = "X-Foo: custom-value"

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"[*] Listening on {LISTEN_IP}:{LISTEN_PORT}")

def insert_custom_header(sip_message: str) -> str:
    # Insert after the first line and before any existing headers
    lines = sip_message.split("\r\n")
    if len(lines) > 1 and lines[0].startswith("INVITE"):
        # Insert after request/status line
        lines.insert(1, X_FOO_HEADER)
    return "\r\n".join(lines)

# Keep a map of clients to respond properly
client_map = {}

while True:
    try:
        data, addr = sock.recvfrom(65535)
        message = data.decode(errors='ignore')
        print(f"\n[>] Received from {addr}:\n{message}")

        if addr == (TARGET_SIP_IP, TARGET_SIP_PORT):
            # Message from SIP server, send it to original client
            client = client_map.get("last_client")
            if client:
                print(f"[<] Forwarding response to {client}")
                sock.sendto(data, client)
        else:
            # Message from SIP client
            client_map["last_client"] = addr
            # Add X-Foo header
            modified_message = insert_custom_header(message)
            print(f"[>>] Forwarding to SIP server {TARGET_SIP_IP}:{TARGET_SIP_PORT}")
            print(f"\n{modified_message}")
            sock.sendto(modified_message.encode(), (TARGET_SIP_IP, TARGET_SIP_PORT))

    except Exception as e:
        print(f"Exception: {e}")
