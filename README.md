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
