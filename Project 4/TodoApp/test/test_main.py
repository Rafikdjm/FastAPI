from fastapi.testclient import TestClient #testclient sert 
# pour simuler des requêtes HTTP vers l'application FastAPI \
# et vérifier les réponses.
from ..main import app # importe l'application FastAPI principale pour les tests.

from fastapi import status# importe les codes de statut HTTP pour les assertions dans les tests.

client = TestClient(app)


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}


