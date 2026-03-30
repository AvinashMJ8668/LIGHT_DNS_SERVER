# servers.py
import socket
import socketserver
import ssl
import struct
import threading
from resolver import process_dns_query
import config

# --- UDP SERVER IMPLEMENTATION ---
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        client_socket = self.request[1]
        response = process_dns_query(data)
        if response:
            client_socket.sendto(response, self.client_address)

def start_udp_server():
    server = socketserver.ThreadingUDPServer((config.HOST, config.UDP_PORT), ThreadedUDPRequestHandler)
    print(f"[*] UDP Server listening on {config.HOST}:{config.UDP_PORT}")
    server.serve_forever()

# --- TLS SERVER IMPLEMENTATION ---
def handle_tls_client(secure_sock, addr):
    print(f"[*] Secure connection from {addr}")
    try:
        length_bytes = secure_sock.recv(2)
        if not length_bytes: return
        msg_length = struct.unpack("!H", length_bytes)[0]
        
        data = secure_sock.recv(msg_length)
        response_data = process_dns_query(data)
        
        if response_data:
            response_length = struct.pack("!H", len(response_data))
            secure_sock.sendall(response_length + response_data)
    except Exception as e:
        print(f"[TLS ERROR] {e}")
    finally:
        secure_sock.close()

def start_tls_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=config.CERT_FILE, keyfile=config.KEY_FILE)
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((config.HOST, config.TLS_PORT))
    server_sock.listen(5)
    
    print(f"[*] TLS Server listening on {config.HOST}:{config.TLS_PORT}")
    
    while True:
        client_sock, addr = server_sock.accept()
        secure_sock = context.wrap_socket(client_sock, server_side=True)
        client_thread = threading.Thread(target=handle_tls_client, args=(secure_sock, addr))
        client_thread.daemon = True
        client_thread.start()