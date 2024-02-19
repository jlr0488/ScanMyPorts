import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target_host, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set a timeout to avoid hanging on inactive ports
            s.settimeout(1)
            # Attempt to connect to the target port
            s.connect((target_host, port))
            # If connection succeeds, the port is open
            print(f"Port {port} is open")
            # Try to receive banner information from the service
            banner = s.recv(1024).decode().strip()
            if banner:
                print(f"  Service running on port {port}: {banner}")
    except (socket.timeout, ConnectionRefusedError):
        # If connection fails or times out, the port is closed
        pass

def scan_host(target_host, ports):
    print(f"Scanning host: {target_host}")
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Scan each port in parallel
        for port in ports:
            executor.submit(scan_port, target_host, port)

def scan_network(network_prefix, ports):
    for host in range(1, 255):
        target_host = f"{network_prefix}.{host}"
        scan_host(target_host, ports)

if __name__ == "__main__":
    # Target host or network to scan
    target = input("Enter target host or network to scan: ")
    # Ports to scan
    ports = [21, 22, 23, 25, 53, 80, 443, 3306, 3389]  # Example ports, you can add more
    if "/" in target:  # If a network is specified
        network_prefix = target.split("/")[0]
        scan_network(network_prefix, ports)
    else:  # If a single host is specified
        scan_host(target, ports)