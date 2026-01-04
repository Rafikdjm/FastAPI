from fastapi import FastAPI
import models
#models sert to create the database tables
from database import engine

from routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
#models.Base.metadata.create_all(bind=engine) : crée les tables dans la base de données
#en utilisant l'engine défini dans database.py

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
#app.include_router permet d'inclure les routeurs définis dans les différents modules