import socket
import threading
import tkinter as tk
from tkinter import messagebox

def scan_ports():
    target = entry_ip.get()
    start_port = int(entry_start.get())
    end_port = int(entry_end.get())

    result_text.delete(1.0, tk.END)  # Efface l'ancienne sortie
    result_text.insert(tk.END, f"Scanning {target} from port {start_port} to {end_port}...\n")

    def scan_single_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((target, port)) == 0:
                result_text.insert(tk.END, f"[+] Port {port} is open\n")
            sock.close()
        except Exception as e:
            pass

    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_single_port, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    messagebox.showinfo("Scan terminé", "Le scan est terminé !")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Scanner de Ports")
root.geometry("400x400")

# Zone pour entrer l'IP
tk.Label(root, text="Adresse IP cible :").pack()
entry_ip = tk.Entry(root)
entry_ip.pack()

# Zone pour entrer le port de départ
tk.Label(root, text="Port de début :").pack()
entry_start = tk.Entry(root)
entry_start.pack()

# Zone pour entrer le port de fin
tk.Label(root, text="Port de fin :").pack()
entry_end = tk.Entry(root)
entry_end.pack()

# Bouton pour démarrer le scan
btn_scan = tk.Button(root, text="Scanner", command=scan_ports)
btn_scan.pack()

# Zone d'affichage des résultats
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Lancement de l'application
root.mainloop()
