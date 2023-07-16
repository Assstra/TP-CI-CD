 ### 14. Ajouter un endpoint /metrics compatible Prometheus (des libs sont disponibles).

 Afin de calculer des metrics pour Prometheus, nous avons utilisé le client officiel Python `prometheus-client`. En particulier, une classe `Counter` utilisée pour calculer le nombre de requêtes et la fonction `generate_latest` qui renvoie les métriques sous forme de string compatible Prometheus.

 Lors de la création d'un `Counter` pour notre application, nous avons ajouté deux labels qui peuvent être utilisées ultérieurement pour filtrer les données de métrique :

 ```python
 http_requests_total = Counter('http_requests_total', 'Requests to city API', ['method', 'code'])
 ```

 Ainsi, chaque fois qu'une requête est faite à l'API, le programme exécute une ligne de code comme celle-ci pour l'enregistrer dans Prometheus :

 ```python
 http_requests_total.labels(method='get', code=200).inc()
 ```

 L'exemple ci-dessus correspond à une requête `GET /city` réussie.

 Tout ce que nous avons à faire dans la requête `GET /metrics` est de renvoyer les métriques sous forme de string à l'aide d'une fonction correspondante :

 ```python
 return generate_latest()
 ```

 ### 15. Ajoutez un Prometheus dans votre docker-compose qui scrappe les métriques de votre application.

 Pour ajouter Prometheus en tant que service dans un fichier *docker-compose.yml* :

 ```yml
   prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./metrics/prometheus.yaml:/etc/prometheus/prometheus.yml
      - prometheus:/prometheus
    ports:
      - ${PROMETHEUS_PORT:?error}:9090
 ```

 Nous ajoutons également une variable d'environnement `PROMETHEUS_PORT` dans le fichier *.env* et un volume `prometheus` à la fin pour éviter de perdre des données de métriques à chaque redémarrage de nos conteneurs :

 ```yml
 volumes:
   prometheus:
 ```

 Enfin, nous créons un fichier *metrics/prometheus.yaml* qui indique à Prometheus où supprimer les métriques (à partir d'un endpoint `python:2022/metrics`) :

 ```yml
 scrape_configs:
   - job_name: city_api
     metrics_path: /metrics
     static_configs:
       - targets:
         - python:2022
         # Same value as in CITY_API_PORT in .env
 ```

 Nous utilisons `python` au lieu de `localhost` puisque tous les services s'exécutent sur le même réseau Docker.

 ### 16. Ajoutez un Grafana dans votre docker-compose et créez y un dahsboard pour monitorer votre application.

 Pour ajouter Grafana à docker-compose :

 ```yml
   grafana:
    image: grafana/grafana:latest
    volumes:
      - ./metrics/datasource.yaml:/etc/grafana/provisioning/datasources/datasource.yaml
      - ./metrics/dashboards.yaml:/etc/grafana/provisioning/dashboards/dashboards.yaml
      - ./metrics/dashboard.json:/var/lib/grafana/dashboards/dashboard.json
    ports:
      - ${GRAFANA_PORT:?error}:3000
```
 Nous devons également ajouter trois fichiers supplémentaires à notre dossier *metrics* :

 1. *datasource.yaml*

 ```yml
 apiVersion: 1

 datasources:
   - name: Prometheus
     type: prometheus
     access: proxy
     isDefault: true
     url: http://prometheus:9090/
 ```
 Ce fichier indique à Grafana où trouver les données de métriques. Dans notre cas, il doit accéder au service `prometheus` sur le même réseau docker sur le port 9090.

 2. *dashboards.yaml*

 ```yml
 apiVersion: 1

 providers:
   - name: 'provisionned dashboards'
     orgId: 1
     folder: ''
     folderUid: ''
     type: file
     disableDeletion: false
     editable: true
     updateIntervalSeconds: 10
     allowUiUpdates: false
     options:
       path: /var/lib/grafana/dashboards
 ```

 Ce fichier indique à Grafana où trouver un fichier JSON pour un dashboard que nous allons créer.

 3. *dashboard.json*

 Ce fichier est l'endroit où nous pouvons enregistrer toutes les configurations de notre dashboard Grafana. Une fois que nous avons créé ou mis à jour un dashboard via l'interface utilisateur Grafana, nous devons aller dans *Dashboard Settings -> JSON Model* et copier un modèle JSON dans le fichier *dashboard.json*. De cette façon, si nous redémarrons les conteneurs, nous pourrons toujours voir le même dashboard dans Grafana.

 **Création d'un dashboard dans Grafana UI**:

 Pour créer un dashboard, nous pouvons simplement aller sur http://localhost:3000, nous connecter avec les identifiants par défaut "admin/admin" et créer un nouveau tableau de bord depuis *Home -> Dashboards* dans *General* ou tout autre dossier.

 Cliquez sur *Add visualization* pour ajouter de nouveaux diagrammes à un dashboard.

Pour notre dashboard, nous avons ajouté trois schémas simples : *Requests per hour*, *Request proportions* et *Scrape duration*.

1. *Requests per hour*:

 Sur la base de la métrique `http_requests_total` que nous avons créée, cette visualisation montre un taux de chaque type de requête dans une plage d'une heure. Le type de requête dépend des deux labels que nous avons ajoutées dans notre application python : "method" et "code". Cela nous permet essentiellement de voir combien de fois par heure chaque demande est effectuée à différents moments.

 2. *Request proportions*:

 Cette visualisation est un graphique en camembert basé sur la même métrique `http_requests_total`, qui compare le nombre total de différents types de requêtes.

 3. *Scrape duration*:

 Cette visualisation est basée sur la métrique interne Prometheus `scrape_duration_seconds` qui stocke une durée de chaque "scrape", càd de chaque collecte des métriques depuis notre endpoint `/metrics`.