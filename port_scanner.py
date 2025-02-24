import socket

def scan_ports(target, start_port, end_port):
    print(f"Scan {target} du port {start_port} au port {end_port}...")
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout pour éviter les blocages
        
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} est ouvert")
        sock.close()

if __name__ == "__main__":
    target_ip = input("Entrée une adresse IP : ")
    start_port = int(input("Entrée le premier port : "))
    end_port = int(input("Entrée le dernier port : "))
    
    scan_ports(target_ip, start_port, end_port)
