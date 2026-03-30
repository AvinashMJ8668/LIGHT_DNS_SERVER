# resolver.py
import socket
from dnslib import DNSRecord, RR, QTYPE, A
import config

def process_dns_query(raw_data):
    try:
        request = DNSRecord.parse(raw_data)
        qname = str(request.q.qname)
        
        # Scenario A: Local Resolution
        if qname in config.LOCAL_RECORDS:
            print(f"[LOCAL] Resolving {qname} -> {config.LOCAL_RECORDS[qname]}")
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(config.LOCAL_RECORDS[qname]), ttl=60))
            return reply.pack()
            
        # Scenario B: Recursive Forwarding
        print(f"[FORWARD] Forwarding {qname} to 8.8.8.8")
        forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forward_sock.settimeout(3.0)
        forward_sock.sendto(raw_data, ("8.8.8.8", 53))
        
        response_data, _ = forward_sock.recvfrom(4096)
        forward_sock.close()
        return response_data

    except Exception as e:
        print(f"[ERROR] Processing failed: {e}")
        return DNSRecord().reply().pack()