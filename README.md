Système de Gestion de Présence des Étudiants — Guide Complet d’Installation et Description du Projet
1. Description du Projet
Ce projet est une application web développée avec Django pour gérer la présence des étudiants en classe. Il permet à un administrateur ou à un enseignant de :

Gérer les étudiants : ajouter, modifier, supprimer des étudiants avec leurs informations (nom, prénom, email, date de naissance, téléphone, numéro d’inscription).

Gérer les classes : créer, modifier, supprimer des classes.

Associer plusieurs classes à un étudiant (relation plusieurs-à-plusieurs).

Marquer la présence : enregistrer la présence ou l'absence des étudiants quotidiennement par classe.

Consulter l’historique de présence : visualiser les présences d’un étudiant sur une période donnée.

Filtrer les étudiants selon différents critères (nom, email, classe, etc.).

Exporter les données de présence au format PDF.

Authentification des utilisateurs : inscription, connexion et gestion des sessions.

Vue calendrier pour visualiser la présence d’un étudiant sur un calendrier.

Interface utilisateur claire et responsive grâce à Tailwind CSS.

2. Technologies et Dépendances
Backend : Django 5.2.x (Python 3.12+ recommandé)

Base de données : PostgreSQL (SQLite possible en développement)

Frontend : Tailwind CSS (pour le style)

Bibliothèques Python :

django (framework web)

psycopg2-binary (adaptateur PostgreSQL)

weasyprint ou reportlab (pour génération de PDF)

django-crispy-forms (optionnel, pour améliorer le rendu des formulaires)

Autres : Git (pour le contrôle de version)

3. Installation et Configuration
Étape 1 : Cloner le projet ou créer un nouveau projet Django
bash
Copy
Edit
git clone https://github.com/VOTRE_UTILISATEUR/votre-projet.git
cd votre-projet
Ou créer un nouveau projet :

bash
Copy
Edit
django-admin startproject attendance_project
cd attendance_project
python manage.py startapp attendance
Étape 2 : Créer et activer un environnement virtuel
bash
Copy
Edit
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
Étape 3 : Installer les dépendances Python
bash
Copy
Edit
pip install django psycopg2-binary weasyprint
Pour crispy forms (optionnel) :

bash
Copy
Edit
pip install django-crispy-forms
Étape 4 : Configurer la base de données PostgreSQL
Installer PostgreSQL.

Créer une base de données et un utilisateur avec mot de passe.

Modifier settings.py pour connecter Django à PostgreSQL :

python
Copy
Edit
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nom_de_votre_db',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Étape 5 : Ajouter Tailwind CSS
Pour une intégration simple, utiliser le CDN dans vos templates HTML :

html
Copy
Edit
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
Pour une intégration avancée, vous pouvez configurer Tailwind avec Node.js (non détaillé ici).

Étape 6 : Ajouter l’application dans INSTALLED_APPS
Dans settings.py :

python
Copy
Edit
INSTALLED_APPS = [
    # Apps Django par défaut
    'attendance',
    # Optionnel
    'crispy_forms',
]
Étape 7 : Exécuter les migrations et créer un super-utilisateur
bash
Copy
Edit
python manage.py makemigrations attendance
python manage.py migrate
python manage.py createsuperuser
Étape 8 : Lancer le serveur de développement
bash
Copy
Edit
python manage.py runserver
L’application sera accessible à l’adresse : http://127.0.0.1:8000

4. Structure des Modèles Principaux
Student (Étudiant)
Champs : first_name, last_name, email (unique), date_of_birth, telephone, roll_number, classrooms (ManyToManyField vers Classroom)

Classroom (Classe)
Champs : name (nom de la classe)

Attendance (Présence)
Champs : student (ForeignKey vers Student), classroom (ForeignKey vers Classroom), date, status (présent/absent)

5. Fonctionnalités Principales
5.1 Gestion des Étudiants
Liste des étudiants avec filtres par nom, email, téléphone, numéro d’inscription et classe.

Pagination.

Création, modification et suppression d’étudiants.

Association d’étudiants à plusieurs classes.

5.2 Gestion des Classes
Liste des classes.

Création, modification et suppression de classes.

5.3 Gestion de la Présence
Saisie quotidienne de la présence par classe.

Saisie de présence individuelle par étudiant, avec sélection de la classe et de la date.

Mise à jour des présences déjà enregistrées.

Consultation de l’historique des présences par étudiant, avec filtres date et classe.

Export au format PDF des présences filtrées.

5.4 Authentification
Pages d’inscription et de connexion.

Restriction d’accès aux fonctionnalités aux utilisateurs authentifiés.

5.5 Vue Calendrier
Visualisation de la présence d’un étudiant sous forme de calendrier coloré (jours présents/absents).

6. Arborescence Exemple du Projet
cpp
Copy
Edit
attendance_project/
│
├── attendance/
│   ├── migrations/
│   ├── templates/
│   │   ├── student_list.html
│   │   ├── classroom_list.html
│   │   ├── mark_attendance.html
│   │   ├── mark_attendance_student.html
│   │   ├── attendance_calendar.html
│   │   ├── login.html
│   │   ├── register.html
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── attendance_project/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
7. Commandes Importantes
Créer migrations :

bash
Copy
Edit
python manage.py makemigrations attendance
Appliquer migrations :

bash
Copy
Edit
python manage.py migrate
Créer un super-utilisateur :

bash
Copy
Edit
python manage.py createsuperuser
Lancer le serveur :

bash
Copy
Edit
python manage.py runserver
