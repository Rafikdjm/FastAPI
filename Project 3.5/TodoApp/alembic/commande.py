#les commandes alembic

#init alembic : alembic init alembic serve a creer le dossier alembic avec les fichiers de configuration

#revision alembic : alembic revision -m "create phone number for user col"  
# permet de creer un fichier de migration avec le message "create phone number for user col"

#upgrade alembic : alembic upgrade head  permet d'appliquer la migration a la base de données en utilisant
# la fonction upgrade()

#downgrade alembic : alembic downgrade -1 permet d'annuler la derniere migration appliquée 
# à la base de données

#head alembic : alembic heads permet de voir la liste des migrations disponibles

#history alembic : alembic history permet de voir l'historique des migrations appliquées

#current alembic : alembic current permet de voir la version actuelle de la base de données

#stamp alembic : alembic stamp head permet de marquer la base de données avec 
# la version actuelle sans appliquer les migrations

#merge alembic : alembic merge -m "merge message" <rev1> <rev2> permet de fusionner
# deux branches de migration
# en une seule avec le message "merge message"
# (utile en cas de conflits de migration)
# pour plus d'informations, consulter la documentation officielle d'alembic


#Pour plus d'informations, consulter la documentation officielle d'alembic :
# https://alembic.sqlalchemy.org/en/latest/index.html
