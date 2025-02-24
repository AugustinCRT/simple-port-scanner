import socket
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv

def start_scan():
    try:
        threading.Thread(target=scan_ports).start()
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

def scan_ports():
    try:
        target = entry_ip.get()
        start_port = int(entry_start.get())
        end_port = int(entry_end.get())

        result_text.delete(1.0, tk.END)  # Efface l'ancienne sortie
        result_text.insert(tk.END, f"Scanning {target} from port {start_port} to {end_port}...\n")

        open_ports = []

        def scan_single_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((target, port)) == 0:
                    service_name = socket.getservbyport(port, "tcp")
                    result_text.insert(tk.END, f"[+] Port {port} is open (Service: {service_name})\n")
                    open_ports.append((port, service_name))
                sock.close()
            except Exception as e:
                pass
            finally:
                progress_bar.step(1)

        total_ports = end_port - start_port + 1
        progress_bar["maximum"] = total_ports
        progress_bar["value"] = 0

        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_single_port, args=(port,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Écrire les résultats dans un fichier CSV si l'option est activée
        if save_to_csv.get():
            with open('scan_results.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Port', 'Service'])
                csvwriter.writerows(open_ports)
            messagebox.showinfo("Scan terminé", "Le scan est terminé ! Les résultats ont été enregistrés dans 'scan_results.csv'.")
        else:
            messagebox.showinfo("Scan terminé", "Le scan est terminé !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Scanner de Ports")
root.geometry("400x400")

# Variable pour suivre l'état de l'option d'enregistrement
save_to_csv = tk.BooleanVar()

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
btn_scan = tk.Button(root, text="Scanner", command=start_scan)
btn_scan.pack()

# Barre de progression
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Zone d'affichage des résultats
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Bouton pour activer ou désactiver l'enregistrement des résultats dans un fichier CSV
chk_save_to_csv = tk.Checkbutton(root, text="Enregistrer les résultats dans un fichier CSV", variable=save_to_csv)
chk_save_to_csv.pack()

# Lancement de l'application
root.mainloop()
