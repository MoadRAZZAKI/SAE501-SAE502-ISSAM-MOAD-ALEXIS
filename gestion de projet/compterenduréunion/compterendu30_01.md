Méthodologie de la gestion de projet  : 

Méthode d'agile 
- Sprint en début de semaine + sprint review en fin de semaine
- Organisation en daily de 15 minutes

on vise a faire une architecture pour notre logiciel :

3 couches  de logiciel 

couche accès aux données : correspond à l'accès à la base de données. 

couche Presentation : présente les données , correspond à l'affichage, et le dialogue avec l'utilisateur

couche Traitement : correspond à la mise en oeuvre de l'ensemble des fonctions et de la logique de l'application.


Description des avancées des étudiants


- Etudiant 1  : 
Sniffer fonctionel : couvre les différents type de paquet DHCP. 
<br/>

Fonctions testées et fonctionnelles:
<br/>
    - Détection automatique des interfaces pour la sélection de l'interface sur laquelle écouter (Linux, MacOS et Windows)
<br/>
    - Filtrage des paquets DHCP uniquement
<br/>
    - Stockage des paquets dans un format adapté (dictionnaire)
<br/>
    - Différentiation des types de paquets DHCP (DHCPOFFER, DHCPREQUEST etc...)
<br/>
    - Extraction automatisée de l'ensemble des données d'un paquet via une fonction qui les intègre dans un dictionnaire




Points suivants à travailler pour la prochaine réunion:
<br/>
    - Filtrage des informations pertinentes en fonction du type de paquet DHCP
    <br/>
    - Filtrage des paquets par séquence de messages
    <br/>
    - Gestion des baux DHCP (creation, renouvellement, expiration)

Axe d'évolution sur le tri des données, voir avec l'étudiant 2 pour des data(s) en json ou txt.

- Etudiant 2 : 
<br/>

Création de l'interface graphique en python (tkinter customisé)
<br/>
Fonctionnalité mise en place  : 
<br/>
    - import,export de data en forma txt ( "","","",",""...)
    <br/>
    - sélection des interfaces 
    <br/>
    - une checkbox pour les serveurs 
     <br/>
    - fonctionnalité de couleur de thème et de zoom.
     <br/>
    - bouton non fonctionel start and stop. 
     <br/>
    - affiche d'info suplémentaire pour chaque paquet 


- Etudiant 3 :

Installation de la base de donnée en Mangodb, sur un environnement Windows et Ubuntu , pour comparer les performances dans les deux OS, pour l'instant , on utilise la base de donnée MONGODB sur windows , et on y accède en utilisant le logiciel mongodbcompass.

Concernant l'api web , j'ai utilisé le framework flask, cette api est directement connecté à la base de données mongodb , elle recupère les données d'une collection spécifique , puis les renvoie en format JSON.

Ce code implémente une architecture modulaire pour une API web. il esty divisé en plusieurs classes selon leur responsabilité : une classe gérant la communication avec la bdd , une autre classe pour récupérer les données ,une troisième pour renvoyer les données au client,et un fichier appsettings.json qui stocke les variables de connexion.






Validatation pour plusieur serveur DHCP avec information sur les plages baux....

Placement du sniffer à définir coté client (en fonction de leur besoin)




