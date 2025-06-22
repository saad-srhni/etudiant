# Système de Gestion de Présence des Étudiants

## Description

Cette application Django permet de gérer la présence des étudiants dans différentes classes avec plusieurs fonctionnalités :

- Gestion des étudiants (ajout, modification, suppression)
- Gestion des classes (création, modification, suppression)
- Association d’un étudiant à plusieurs classes
- Marquage quotidien des présences par classe et par étudiant
- Consultation de l’historique des présences
- Filtrage avancé des étudiants (nom, email, téléphone, classe, etc.)
- Export des présences au format PDF
- Authentification utilisateur (inscription, connexion, déconnexion)
- Vue calendrier pour visualiser la présence par étudiant
- Interface responsive avec Tailwind CSS

---

## Technologies utilisées

- Python 3.12+
- Django 5.2.x
- SQLite (par défaut) ou PostgreSQL (production)
- Tailwind CSS
- WeasyPrint (pour export PDF)
- Autres bibliothèques Python (django-crispy-forms optionnel)

---

## Installation

1- Créer et activer un environnement virtuel

python -m venv env
# Linux / Mac
source env/bin/activate
# Windows
env\Scripts\activate

2- Installer les dépendances

pip install -r requirements.txt
Configurer la base de données

3- Modifier attendance_project/settings.py si besoin (par défaut SQLite).

Appliquer les migrations

python manage.py migrate
Créer un super-utilisateur

python manage.py createsuperuser
Lancer le serveur

python manage.py runserver
Accéder à http://127.0.0.1:8000/students


