# main.py
import threading
from servers import start_udp_server, start_tls_server

if __name__ == "__main__":
    print("Starting Custom DNS Server...")
    
    # Start UDP in a background thread
    udp_thread = threading.Thread(target=start_udp_server)
    udp_thread.daemon = True
    udp_thread.start()
    
    # Start TLS in the main thread to keep the program running
    try:
        start_tls_server()
    except KeyboardInterrupt:
        print("\nShutting down servers...")