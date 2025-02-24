import socket
import threading

def scan_single_port(target, port, open_ports):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Timeout pour éviter les blocages
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"[+] Port {port} est ouvert")
                open_ports.append(port)
        except socket.error as e:
            print(f"Erreur de connexion au port {port}: {e}")

def scan_ports(target, start_port, end_port):
    print(f"Scan de {target} du port {start_port} au port {end_port}...")
    open_ports = []
    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_single_port, args=(target, port, open_ports))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"Scan terminé. {len(open_ports)} ports ouverts trouvés.")

if __name__ == "__main__":
    try:
        target_ip = input("Entrez une adresse IP : ")
        start_port = int(input("Entrez le premier port : "))
        end_port = int(input("Entrez le dernier port : "))
        
        if start_port < 0 or end_port < 0 or start_port > end_port:
            raise ValueError("Les numéros de port doivent être positifs et le premier port doit être inférieur ou égal au dernier port.")
        
        scan_ports(target_ip, start_port, end_port)
    except ValueError as ve:
        print(f"Erreur d'entrée : {ve}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
