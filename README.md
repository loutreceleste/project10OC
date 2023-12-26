# Projet 10 Création d'une API avec Django REST Framework OpenClassrooms
Ce projet consiste à créer une API fictive en utilisant le framework Django REST dans le cadre de ma formation Python chez OpenClassrooms. En tant qu'ingénieur logiciel chez Softdesk (une entreprise fictive), ma mission est de développer un backend performant et sécurisé destiné à être utilisé par des applications frontend sur différentes plateformes.
## Installation
### Cloner le dépôt :

```bash
git clone https://github.com/loutreceleste/project10OC.git
````
```bash
cd project10OC/softdesk
```
### Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation
### Exécuter les migrations :

```bash
python manage.py migrate
```
### Démarrer le serveur :

```bash
python manage.py runserver
```
Pour explorer et interagir avec les fonctionnalités de cette API, nous vous invitons à vous référer à la rubrique « Exemples d'Utilisation ».
## Exemples d'Utilisation
Exemple de Requête GET
```bash
curl http://localhost:8000/api/issues
```
Exemple de Requête POST avec données JSON
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "Identification",
    "nature": "BU",
    "priority": "ME",
    "progression": "TD",
    "description": "Impossibilité de s'autentifier sur l'application",
    "contributors": [1, 7]
}' http://localhost:8000/api/projects/1/issues
```
Nous vous présentons des exemples de requêtes exécutées via le terminal. Cependant, pour une interaction plus conviviale avec notre API, nous vous recommandons d'utiliser des outils spécialisés tels que Postman ou Insomnia et de vous referer a la documentation mise à disposition. Ces logiciels offrent une interface conviviale pour interagir avec les endpoints de l'API, ce qui facilite la manipulation des requêtes HTTP ainsi que l'observation des réponses fournies par l'API.

## Documentation
Une fois que vous avez démarré le serveur, la documentation complète de l'API est disponible ici http://127.0.0.1:8000/swagger/. Vous y trouverez des informations détaillées sur les endpoints, les paramètres, les réponses attendues, et des exemples d'utilisation.

## Contributions
Les contributions sont les bienvenues ! Veuillez ouvrir une issue pour discuter des changements importants que vous souhaitez apporter.

## Licence
Ce projet est sous licence MIT License.
