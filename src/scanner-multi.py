import socket
import sys
import threading

# On verifie qu'il y a bien un argument
if len(sys.argv) != 2:
    print("Usage: python scanner.py <target ip or hostname>")
    sys.exit()

cible = sys.argv[1]

# On transforme le nom de domaine en adresse IP
try:
    ip = socket.gethostbyname(cible)
except socket.gaierror as erreur:
    print("Hostname could not be resolved:", erreur)
    sys.exit()

# La liste ou les threads vont ranger les ports ouverts
ports_ouverts = []


# Ce que chaque thread va faire : tester UN seul port
def tester_port(port):
    # Le "with" ferme le socket meme en cas d'erreur
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        resultat = s.connect_ex((ip, port))
        if resultat == 0:
            ports_ouverts.append(port)


print("Scanning " + cible + "...")

try:
    # On scanne par groupes de 100 ports : 1-100, 101-200, etc.
    for debut in range(1, 1024, 100):
        fin = min(debut + 100, 1024)
        threads = []

        # On lance un thread pour chaque port du groupe
        for port in range(debut, fin):
            t = threading.Thread(target=tester_port, args=(port,))
            # Le thread s'arrete avec le programme (utile pour CTRL+C)
            t.daemon = True
            t.start()
            threads.append(t)

        # On attend que tous les threads du groupe aient fini
        for t in threads:
            t.join()
except KeyboardInterrupt:
    print("Scan is stopping...")

# On affiche les ports ouverts dans l'ordre
ports_ouverts.sort()
for port in ports_ouverts:
    print("--> Port " + str(port) + "/TCP is open.")

print("Scan completed successfully.")