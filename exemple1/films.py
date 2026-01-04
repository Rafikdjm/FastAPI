"""
EXERCICES FASTAPI - GESTION D'UNE BIBLIOTHÈQUE DE FILMS
========================================================

Base de données initiale:
"""

from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

MOVIES = [
    {'id': 1, 'title': 'Inception', 'director': 'Christopher Nolan', 'year': 2010, 'genre': 'sci-fi', 'rating': 8.8},
    {'id': 2, 'title': 'The Matrix', 'director': 'Wachowski', 'year': 1999, 'genre': 'sci-fi', 'rating': 8.7},
    {'id': 3, 'title': 'Pulp Fiction', 'director': 'Quentin Tarantino', 'year': 1994, 'genre': 'crime', 'rating': 8.9},
    {'id': 4, 'title': 'The Godfather', 'director': 'Francis Ford Coppola', 'year': 1972, 'genre': 'crime', 'rating': 9.2},
    {'id': 5, 'title': 'Interstellar', 'director': 'Christopher Nolan', 'year': 2014, 'genre': 'sci-fi', 'rating': 8.6},
    {'id': 6, 'title': 'Forrest Gump', 'director': 'Robert Zemeckis', 'year': 1994, 'genre': 'drama', 'rating': 8.8}
]

"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 1: GET - Récupérer tous les films
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Créer un endpoint qui retourne tous les films

ÉTAPES:
1. Utiliser le décorateur @app.get() avec le chemin "/movies"
2. Définir une fonction asynchrone
3. Retourner la liste MOVIES
4. Ajouter un status_code 200

SOLUTION:
"""

@app.get("/movies", status_code=status.HTTP_200_OK)
async def get_all_movies():
    return MOVIES


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 2: GET avec Path Parameter - Récupérer un film par ID
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Récupérer un film spécifique par son ID

ÉTAPES:
1. Utiliser {movie_id} dans le chemin pour créer un paramètre dynamique
2. Ajouter une validation avec Path(gt=0) pour accepter seulement les ID > 0
3. Parcourir la liste MOVIES pour trouver le film
4. Lever une HTTPException si le film n'existe pas

SOLUTION:
"""

@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK)
async def get_movie_by_id(movie_id: int = Path(gt=0)):
    for movie in MOVIES:
        if movie['id'] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail='Film non trouvé')


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 3: GET avec Query Parameter - Filtrer par genre
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Récupérer tous les films d'un genre spécifique

ÉTAPES:
1. Utiliser "/movies/" (avec slash final) pour différencier des path parameters
2. Ajouter un paramètre de query "genre"
3. Filtrer les films qui correspondent au genre (case insensitive)
4. Retourner la liste filtrée

SOLUTION:
"""

@app.get("/movies/", status_code=status.HTTP_200_OK)
async def get_movies_by_genre(genre: str):
    movies_to_return = []
    for movie in MOVIES:
        if movie['genre'].casefold() == genre.casefold():
            movies_to_return.append(movie)
    return movies_to_return


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 4: GET avec Query Parameter validé - Filtrer par note
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Récupérer les films avec une note minimale

ÉTAPES:
1. Utiliser Query() pour ajouter des validations
2. Valider que min_rating est entre 0 et 10
3. Filtrer les films ayant une note >= min_rating
4. Retourner les films filtrés

SOLUTION:
"""

@app.get("/movies/rating/", status_code=status.HTTP_200_OK)
async def get_movies_by_rating(min_rating: float = Query(ge=0, le=10)):
    movies_to_return = []
    for movie in MOVIES:
        if movie['rating'] >= min_rating:
            movies_to_return.append(movie)
    return movies_to_return


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 5: GET avec multiples Query Parameters - Filtrage avancé
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Filtrer par réalisateur ET année

ÉTAPES:
1. Créer un endpoint avec deux query parameters: director et year
2. Filtrer les films qui correspondent aux deux critères
3. Utiliser casefold() pour le réalisateur
4. Retourner la liste filtrée

SOLUTION:
"""

@app.get("/movies/search/", status_code=status.HTTP_200_OK)
async def get_movies_by_director_and_year(director: str, year: int = Query(gt=1900, lt=2030)):
    movies_to_return = []
    for movie in MOVIES:
        if movie['director'].casefold() == director.casefold() and movie['year'] == year:
            movies_to_return.append(movie)
    return movies_to_return


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 6: POST avec Pydantic - Créer un nouveau film
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Ajouter un nouveau film avec validation des données

ÉTAPES:
1. Créer une classe MovieRequest héritant de BaseModel
2. Définir les champs avec des validations (Field)
3. Créer un endpoint POST
4. Convertir le MovieRequest en dictionnaire
5. Générer un nouvel ID automatiquement
6. Ajouter le film à MOVIES

SOLUTION:
"""

class MovieRequest(BaseModel):
    id: Optional[int] = Field(default=None, description="ID généré automatiquement")
    title: str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=1, max_length=50)
    year: int = Field(gt=1888, lt=2030, description="Année de sortie du film")
    genre: str = Field(min_length=3, max_length=20)
    rating: float = Field(ge=0, le=10, description="Note entre 0 et 10")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Shawshank Redemption",
                "director": "Frank Darabont",
                "year": 1994,
                "genre": "drama",
                "rating": 9.3
            }
        }
    }


@app.post("/movies/create", status_code=status.HTTP_201_CREATED)
async def create_movie(movie_request: MovieRequest):
    new_movie = movie_request.model_dump()
    # Générer un nouvel ID
    new_movie['id'] = 1 if len(MOVIES) == 0 else MOVIES[-1]['id'] + 1
    MOVIES.append(new_movie)
    return new_movie


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 7: PUT - Mettre à jour un film existant
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Modifier un film existant par son ID

ÉTAPES:
1. Créer un endpoint PUT
2. Accepter un MovieRequest avec un ID obligatoire
3. Chercher le film dans MOVIES
4. Remplacer le film si trouvé
5. Lever une exception si non trouvé

SOLUTION:
"""

@app.put("/movies/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(movie: MovieRequest):
    if movie.id is None:
        raise HTTPException(status_code=400, detail="ID requis pour la mise à jour")
    
    movie_found = False
    for i in range(len(MOVIES)):
        if MOVIES[i]['id'] == movie.id:
            MOVIES[i] = movie.model_dump()
            movie_found = True
            break
    
    if not movie_found:
        raise HTTPException(status_code=404, detail='Film non trouvé')


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICE 8: DELETE - Supprimer un film
═══════════════════════════════════════════════════════════════════════════════

OBJECTIF: Supprimer un film par son ID

ÉTAPES:
1. Créer un endpoint DELETE avec path parameter
2. Valider l'ID avec Path(gt=0)
3. Chercher et supprimer le film
4. Utiliser break pour sortir de la boucle après suppression
5. Lever une exception si non trouvé

SOLUTION:
"""

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int = Path(gt=0)):
    movie_deleted = False
    for i in range(len(MOVIES)):
        if MOVIES[i]['id'] == movie_id:
            MOVIES.pop(i)
            movie_deleted = True
            break
    
    if not movie_deleted:
        raise HTTPException(status_code=404, detail='Film non trouvé')


"""
═══════════════════════════════════════════════════════════════════════════════
EXERCICES À FAIRE VOUS-MÊME
═══════════════════════════════════════════════════════════════════════════════

EXERCICE A: Créer un endpoint GET qui retourne tous les films d'une décennie
- Chemin: /movies/decade/
- Query parameter: decade (ex: 1990, 2000, 2010)
- Retourner les films dont l'année est entre decade et decade+9
solution:
@app.get("/movies/decade/", status_code=status.HTTP_200_OK)
async def get_movies_by_decade(decade: int = Query(..., ge=1900 )):
    movies_to_return = []
    for movie in MOVIES:
        if decade <= movie['year'] <= decade + 9:
            movies_to_return.append(movie)
    return movies_to_return
    

EXERCICE B: Créer un endpoint GET qui retourne les films triés par note
- Chemin: /movies/top/
- Query parameter optionnel: limit (nombre de films à retourner, défaut=10)
- Retourner les films triés du mieux noté au moins bien noté
solution:

@app.get("/movies/top/", status_code=status.HTTP_200_OK)
async def get_top_movies(limit: int = Query(10, gt=0)):
    sorted_movies = sorted(MOVIES, key=lambda x: x['rating'], reverse=True) 
    return sorted_movies[:limit]
    

EXERCICE C: Créer un endpoint PATCH pour mettre à jour seulement la note
- Chemin: /movies/{movie_id}/rating
- Body: nouvelle note (float entre 0 et 10)
- Mettre à jour uniquement le champ rating du film

solution:
@app.patch("/movies/{movie_id}/rating", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie_rating(movie_id: int = Path(gt=0), new_rating: float = Body(..., ge=0, le=10)):
    movie_found = False
    for i in range(len(MOVIES)):
        if MOVIES[i]['id'] == movie_id:
            MOVIES[i]['rating'] = new_rating
            movie_found = True
            break
    
    if not movie_found:
        raise HTTPException(status_code=404, detail='Film non trouvé')
        
        
        
        
EXERCICE D: Créer un endpoint GET avec plusieurs filtres optionnels
- Chemin: /movies/filter/
- Query parameters optionnels: genre, min_year, max_year, min_rating
- Retourner les films qui correspondent à TOUS les critères fournis

solution:
@app.get("/movies/filter/", status_code=status.HTTP_200_OK)
async def filter_movies(
    genre: Optional[str] = None,
    min_year: Optional[int] = Query(None, gt=1900),
    max_year: Optional[int] = Query(None, lt=2030),
    min_rating: Optional[float] = Query(None, ge=0, le=10)
):
    movies_to_return = []
    for movie in MOVIES:
        if genre and movie['genre'].casefold() != genre.casefold():
            continue
        if min_year and movie['year'] < min_year:
            continue
        if max_year and movie['year'] > max_year:
            continue
        if min_rating and movie['rating'] < min_rating:
            continue
        movies_to_return.append(movie)
    return movies_to_return


═══════════════════════════════════════════════════════════════════════════════
CONCEPTS CLÉS À RETENIR
═══════════════════════════════════════════════════════════════════════════════

1. PATH PARAMETERS vs QUERY PARAMETERS:
   - Path: /movies/{movie_id} → Identifie UNE ressource spécifique
   - Query: /movies/?genre=sci-fi → Filtre ou recherche des ressources

2. VALIDATIONS:
   - Path(gt=0) : greater than (plus grand que)
   - Query(ge=0, le=10) : greater/less or equal (supérieur/inférieur ou égal)
   - Field(min_length=3, max_length=100) : longueur de chaîne

3. STATUS CODES HTTP:
   - 200 OK : Succès général (GET)
   - 201 CREATED : Ressource créée (POST)
   - 204 NO CONTENT : Succès sans contenu (PUT, DELETE)
   - 404 NOT FOUND : Ressource non trouvée

4. PYDANTIC:
   - BaseModel : Classe de base pour la validation
   - Field : Définir contraintes et métadonnées
   - model_dump() : Convertir le modèle en dictionnaire

5. BONNES PRATIQUES:
   - Toujours valider les entrées utilisateur
   - Utiliser des HTTPException pour les erreurs
   - Utiliser casefold() pour les comparaisons insensibles à la casse
   - Ajouter des status codes appropriés

6- le patch :
    - Utilisé pour les mises à jour partielles
    - Permet de modifier seulement certains champs d'une ressource
    - Utile pour éviter d'envoyer l'intégralité de la ressource lors d'une modification mineure
    - Souvent utilisé pour des mises à jour rapides et ciblées
    - Doit être utilisé avec précaution pour s'assurer que seules les parties nécessaires sont modifiées
7- tri et filtres avancés :
    - Permet de combiner plusieurs critères de recherche
    - Utile pour les applications avec de grandes bases de données
    - Améliore l'expérience utilisateur en fournissant des résultats pertinents
    - Peut inclure des paramètres optionnels pour plus de flexibilité
    - Nécessite une logique de filtrage claire et efficace dans le code
8- gestion des erreurs :
    - Essentielle pour une API robuste
    - Utiliser HTTPException pour renvoyer des messages d'erreur clairs
    - Aide à diagnostiquer les problèmes côté client
    - Permet de gérer les cas où les ressources ne sont pas trouvées ou les entrées sont invalides
    - Améliore la fiabilité et la maintenabilité de l'API
9- documentation automatique :
    - FastAPI génère automatiquement la documentation interactive
    - Utilise OpenAPI et Swagger UI
    - Permet aux développeurs de tester les endpoints directement depuis le navigateur
    - Facilite la compréhension de l'API pour les utilisateurs finaux
    - Encourage les bonnes pratiques de développement API
10- performance et scalabilité :
    - FastAPI est conçu pour être rapide et efficace
    - Utilise Starlette pour la gestion asynchrone des requêtes
    - Convient aux applications à fort trafic
    - Permet de gérer de nombreuses connexions simultanées
    - Idéal pour les microservices et les architectures distribuées
"""