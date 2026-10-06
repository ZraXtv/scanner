# Travail Pratique #1: TCP Port Scanner

## Auteurs
- PELV07030600, Pellé, Victor
- ROUF30040400, Roux, Fabien

## Compatibilité

Python - 3.8 (ou toute version plus récente)

Le script fonctionne sous Linux, macOS et Windows.

## Description

Application console (CLI) qui scanne les ports TCP réservés (1 à 1023) d'une machine cible et affiche ceux qui sont ouverts. La cible peut être une adresse IP ou un nom de domaine.

## Utilisation

### Prérequis

1. Installer Python 3.8 ou plus récent : https://www.python.org/downloads/
2. Vérifier l'installation :
   ```bash
   python3 --version
   ```
   Sous Windows, utiliser `python` au lieu de `python3`.

Aucune dépendance à installer : le script utilise uniquement la librairie standard de Python (`socket` et `sys`). Aucune commande `pip install` n'est nécessaire.

### Lancer le scanner

Depuis le dossier `scanner/` :

```bash
python3 src/scanner.py <target ip or hostname>
```

Exemples :

```bash
python3 src/scanner.py 192.168.0.1
python3 src/scanner.py localhost
```

### Exemple de sortie

```
$> python3 src/scanner.py 192.168.0.1
Scanning 192.168.0.1...
--> Port 22/TCP is open.
--> Port 80/TCP is open.
Scan completed successfully.
```

### Gestion des erreurs

Sans paramètre, le programme affiche son utilisation :
```
$> python3 src/scanner.py
Usage: python scanner.py <target ip or hostname>
```

Avec un nom de domaine invalide, le programme affiche l'erreur et s'arrête :
```
$> python3 src/scanner.py wrongdomain.name
Hostname could not be resolved: [Errno -2] Name or service not known
```
Le message exact dépend du système d'exploitation (par exemple `[Errno 11001] getaddrinfo failed` sous Windows).

Avec un CTRL+C pendant le scan, le programme s'arrête proprement :
```
$> python3 src/scanner.py 192.168.0.1
Scanning 192.168.0.1...
Scan is stopping...
Scan completed successfully.
```

## Fonctionnement

1. Le nom de domaine est converti en adresse IP avec `socket.gethostbyname()`.
2. Pour chaque port de 1 à 1023, un socket TCP est créé et tente une connexion avec `connect_ex()`.
3. Si `connect_ex()` renvoie `0`, la connexion a réussi : le port est ouvert et il est affiché. Les ports fermés ne sont pas affichés.
4. Un délai d'attente de 0,5 seconde est appliqué à chaque port pour ne pas bloquer sur les machines qui ne répondent pas.

Durée du scan : quelques secondes sur une machine du réseau local qui refuse les connexions. Jusqu'à environ 8 minutes si la cible ne répond pas du tout (1023 ports × 0,5 seconde).

## Bonus : version multi-threadée

Une seconde version du scanner, multi-threadée, se trouve dans `src/scanner-multi.py`. Elle s'utilise exactement comme la version normale, avec la même gestion des erreurs et du CTRL+C :

```bash
python3 src/scanner-multi.py <target ip or hostname>
```

Fonctionnement :

1. Les ports 1 à 1023 sont scannés par groupes de 100 ports (1-100, 101-200, etc.).
2. Pour chaque port du groupe, un thread (`threading.Thread`) est lancé et teste ce port avec `connect_ex()`, comme dans la version normale.
3. Le programme attend la fin de tous les threads du groupe (`join()`) avant de passer au groupe suivant. Cela limite le nombre de sockets ouverts en même temps.
4. Les ports ouverts sont stockés dans une liste, triée puis affichée à la fin du scan. Les ports s'affichent donc dans l'ordre, une fois le scan terminé, et non au moment où ils sont trouvés.

Durée du scan : environ 6 secondes au maximum si la cible ne répond pas du tout (11 groupes × 0,5 seconde), contre environ 8 minutes pour la version normale.

## Avertissement

Au Canada, scanner les ports d'une machine sans autorisation préalable est illégal. Ce programme a été testé uniquement sur des machines de notre réseau local.