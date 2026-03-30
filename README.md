# LIGHT_DNS_SERVER (UDP & DoT)

A lightweight, multi-threaded DNS server implemented in Python. This project supports both standard DNS queries over UDP (Port 53) and secure DNS over TLS (DoT) queries (Port 853). It features local record resolution and recursive forwarding for external domains.

## Features
* **Dual Protocol Support:** Handles standard UDP requests and encrypted TLS connections simultaneously using Python threading.
* **DNS over TLS (DoT):** Secures DNS queries using SSL/TLS encryption.
* **Local Resolution:** Resolves predefined local domains (e.g., `mycustomdomain.local`) from a configuration file.
* **Recursive Forwarding:** Unrecognized queries are automatically forwarded to public DNS resolvers (e.g., Google's `8.8.8.8`).
* **Interactive Testing Client:** Includes a custom client script to test both UDP and TLS query routing.

## Prerequisites
* Python 3.x
* `dnslib` package
* OpenSSL (for generating local certificates)

Install the required Python dependency:
```bash
pip install dnslib

Clone the repository:
git clone [https://github.com/AvinashMJ8668/LIGHT_DNS_SERVER.git](https://github.com/AvinashMJ8668/LIGHT_DNS_SERVER.git)
cd LIGHT_DNS_SERVER

Generate SSL/TLS Certificates:
For security reasons, the private keys and certificates are not included in this repository. You must generate your own self-signed certificates to run the TLS server. Run the following OpenSSL command in the project root:
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

1. Start the Server:
Run main.py with administrator/root privileges (required to bind to port 53 and 853):
sudo python main.py
On Windows, open your command prompt or terminal as Administrator and run python main.py

2. Run the Interactive Client:
python test_client.py


