import socket
import ssl
import struct
from dnslib import DNSRecord

SERVER_IP = "127.0.0.1"
UDP_PORT = 53
TLS_PORT = 853

def test_udp(domain):
    print(f"\n--- Testing UDP (Port {UDP_PORT}) for {domain} ---")
    try:
        query = DNSRecord.question(domain)
        query_data = query.pack()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3.0)
        sock.sendto(query_data, (SERVER_IP, UDP_PORT))

        response_data, _ = sock.recvfrom(4096)
        response = DNSRecord.parse(response_data)
        
        print("[SUCCESS] Received UDP Response:")
        print(response)
        sock.close()
    except Exception as e:
        print(f"[FAILED] UDP Test Error: {e}")

def test_tls(domain):
    print(f"\n--- Testing TLS/DoT (Port {TLS_PORT}) for {domain} ---")
    try:
        query = DNSRecord.question(domain)
        query_data = query.pack()
        
        length_prefix = struct.pack("!H", len(query_data))
        full_message = length_prefix + query_data

        context = ssl._create_unverified_context()

        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_sock.settimeout(3.0)
        secure_sock = context.wrap_socket(raw_sock, server_hostname=SERVER_IP)
        secure_sock.connect((SERVER_IP, TLS_PORT))

        secure_sock.sendall(full_message)

        response_length_bytes = secure_sock.recv(2)
        if not response_length_bytes:
            raise Exception("Server closed connection without sending length prefix")
        
        response_length = struct.unpack("!H", response_length_bytes)[0]

        response_data = secure_sock.recv(response_length)
        response = DNSRecord.parse(response_data)

        print("[SUCCESS] Received TLS Response:")
        print(response)
        secure_sock.close()
    except Exception as e:
        print(f"[FAILED] TLS Test Error: {e}")

if __name__ == "__main__":
    print("Starting Interactive DNS Client...")
    print(f"Connecting to Server at: {SERVER_IP}")
    
    while True:
        try:
            print("\n" + "="*40)
            # Take domain input from the terminal
            domain = input("Enter domain to resolve (or type 'quit' to exit): ").strip()
            
            if domain.lower() in ['quit', 'exit', 'q']:
                print("Exiting client. Goodbye!")
                break
                
            if not domain:
                print("Domain cannot be empty. Please try again.")
                continue

            # Ask the user which protocol to use
            protocol = input("Use (U)DP or (T)LS? [U/T]: ").strip().upper()

            if protocol == 'U':
                test_udp(domain)
            elif protocol == 'T':
                test_tls(domain)
            else:
                print("Invalid choice. Please enter 'U' for UDP or 'T' for TLS.")
                
        # Handle Ctrl+C gracefully
        except KeyboardInterrupt:
            print("\nExiting client. Goodbye!")
            break