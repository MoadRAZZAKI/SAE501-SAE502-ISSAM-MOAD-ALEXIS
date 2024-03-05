## installation de l'image docker 

- Dans le fichier /Docker-Mongo/docker-compose.yml se trouve le code pour lancer une instance MongoDB avec authentification et réplication de données,

## lancement de l'image docker 

- on redémarre le service Docker : avec la commande suivante 

```
sudo systemctl restart docker
```

- ensuite , on utilise OpenSSL pour générer une clé aléatoire de 756 bits et la stocke dans un fichier mongo-keyfile. Cette clé va être utilisée après pour l'authentification entre les membres d'un réplica set MongoDB.

```
sudo openssl rand -base64 756 > mongo-keyfile
```


- on utilise la commande chmod pour modifier les permissions du fichier mongo-keyfile pour restreindre l'accès uniquement au propriétaire du fichier


```
chmod 600 mongo-keyfile
```

- ensuite, on démarre les services définis dans le fichier docker-compose.yml en utilisant la commande docker-compose : 

```
docker-compose up -d
```

- on accède au shell du conteneur


```
docker exec -it mongodb /bin/bash
```

- on lance ensuite le shell de la mongodb: 

```
mongosh --username root --password password
```

- enfin, on va initier un nouveau réplica set MongoDB. Un réplica set est un ensemble de processus MongoDB qui maintiennent les mêmes données pour assurer la redondance et la disponibilité des données: 

```
rs.initiate()
```

- si le replica est en Secondary , on se déconnecte du shell mongodb et du shell docker , et on se reconnecte , cela permet de régler le problème .

- n'oubliez pas d'ajouter l'ip de la machine hôte pour permettre aux machines du même réseau d'interroger la bdd : 

```
rs.add({host:"10.203.0.149:27017",votes: 1})
```
