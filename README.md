# TP-CI-CD

## Information générales

Group:
- Adrien Raimbault
- Dziyana Tsetserava
- Muriel Paraire


Langage de programmation choisie:
- Python


## Questions

### 1. Créez un fichier docker-compose.yml et ajoutez-y un service db s'appuyant sur l'imageDocker postrges:latest.

Nous avons donc crée un service de nom db de manière suivante :
```yml
services:
  db:
    # utiliser la dernière image postgres
    image: postgres:latest
    # redemarrer en cas d'échec ou de crash
    restart: always
    # prise en compte des valeurs précisé par l'utilisateur
    environment:
      - POSTGRES_PASSWORD=${CITY_API_DB_PWD:?error}
      - POSTGRES_USER=${CITY_API_DB_USER?:error}
      - POSTGRES_DB=city_api
    # le port sur lequel on peut joindre la base de données
    expose:
      - ${CITY_API_DB_PORT:?error}
    volumes:
      # l'endroit de sauvegarde
      - /var/lib/postgres
      # le script pour créer la table city
      - ./db/init.sql:/docker-entrypoint-initdb.d/create_city.sql
      # le script pour insérer les données
      - ./db/populate.sql:/docker-entrypoint-initdb.d/populate_city.sql
```

Par la suite, nous avons aussi completé notre fichier docker-compose.yml pour y ajouter un containeur démarrons notre API : 

```yml
  python:
    # le dockerfile pour lancer l'application
    build:
      context: .
      dockerfile: python.dockerfile
    # le fichier d'environnement
    env_file:
      - .env
    # l'api a besoin que la base de données sois créer pour pouvoir l'utiliser
    depends_on:
      - postgres
```

### 2. Créez une base de données  city_api  avec une table  city  contenant les colonnes suivantes :
- **id** , un entier non signé non nul, clé primaire de la colonne ;
- ***department_code** , une chaîne de caractères non nulle ;
- **insee_code** , une chaîne de caractères ;
- **zip_code** , une chaîne de caractères ;
name , une chaîne de caractères non nulle ;
lat , un flottant non nul ;
lon , un flottant non nul.