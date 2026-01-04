from sqlalchemy import create_engine # SQLAlchemy est un ORM (Object Relational Mapper)
#create_engine permet de créer une connexion à la base de données

from sqlalchemy.orm import sessionmaker #.orm permet de créer des sessions pour interagir
#avec la base de données
#sessionmaker permet de créer des objets de session

from sqlalchemy.ext.declarative import declarative_base 
#.ext.declarative permet de définir des classes de base pour les modèles de données
#declarative_base permet de créer une classe de base pour les modèles de données

# sqlalchemy sert pour interagir avec la base de données SQLite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

# Encoder le mot de passe
password = quote_plus("RafikDM@06")
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{password}@localhost/TodoApplicationServer'



#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

#connect_args={'check_same_thread': False} : option spécifique à SQLite pour permettre
#à plusieurs threads d'accéder à la même connexion de base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL) # création de l'engine pour PostgreSQL


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# autocommit=False : les modifications ne sont pas automatiquement enregistrées
# autoflush=False : les modifications ne sont pas automatiquement envoyées à la base de données
# bind=engine : lie la session à l'engine créé précédemment
Base = declarative_base()
