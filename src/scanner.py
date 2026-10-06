import socket
import sys

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

print("Scanning " + cible + "...")

# On teste les ports 1 a 1023 un par un
try:
    for port in range(1, 1024):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        resultat = s.connect_ex((ip, port))
        if resultat == 0:
            print("--> Port " + str(port) + "/TCP is open.")
        s.close()
except KeyboardInterrupt:
    print("Scan is stopping...")

print("Scan completed successfully.")