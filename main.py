"""
Fichier : main.py
Rôle :
Ce fichier contient l’API REST du projet "Recommandations de santé".

Fonctionnement :
- L’API est développée avec FastAPI.
- Les recommandations sont stockées dans un fichier local JSON.
- L’API permet d’afficher toutes les recommandations.
- L’API permet aussi de filtrer par catégorie, sous-catégorie et public.
- Une route permet d’afficher une recommandation précise à partir de son id.

Dépendances :
- FastAPI : création de l’API REST
- CORSMiddleware : autorisation des appels depuis le portfolio
- json : lecture du fichier recommandations.json
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

# Création de l’application FastAPI
app = FastAPI()

"""
Configuration CORS :
Le CORS permet au front-end du portfolio hébergé sur Alwaysdata
d’appeler l’API hébergée sur Render.

Sans cette configuration, le navigateur pourrait bloquer les requêtes
entre deux domaines différents.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Autorise les appels depuis tous les domaines
    allow_credentials=True,
    allow_methods=["*"],       # Autorise toutes les méthodes HTTP
    allow_headers=["*"],       # Autorise tous les en-têtes
)

def charger_recommandations():
    """
    Fonction : charger_recommandations()
    Rôle :
    Lire le fichier recommandations.json et retourner son contenu.

    
    vue que les recommandations sont stockées dans un fichier JSON local.
    Cette fonction centralise la lecture du fichier afin d’éviter de répéter
    le même code dans chaque route.
    """
    with open("recommandations.json", "r", encoding="utf-8") as fichier:
        return json.load(fichier)

@app.get("/")
def accueil():
    """
    Route d’accueil de l’API.
    Elle permet simplement de vérifier que l’API fonctionne.
    """
    return {"message": "API Recommandations de santé"}

@app.get("/api/recommandations")
def get_recommandations(categorie: str = None, sousCategorie: str = None, public: str = None):
    """
    Route : GET /api/recommandations

    elle a comme role de retourner toutes les recommandations ou filtrer les résultats
    selon les paramètres envoyés dans l’URL.

    Paramètres possibles :
    - categorie
    - sousCategorie
    - public

    
    comme par exemple:/api/recommandations?categorie=Alimentation&public=Adultes
    """

    # Chargement de toutes les recommandations depuis le fichier JSON
    varRecommandations = charger_recommandations()

    # Filtrage par catégorie si le paramètre est présent dans l’URL
    if categorie:
        varRecommandations = [
            varReco for varReco in varRecommandations
            if varReco["categorie"].lower() == categorie.lower()
        ]

    # Filtrage par sous-catégorie si le paramètre est présent dans l’URL
    if sousCategorie:
        varRecommandations = [
            varReco for varReco in varRecommandations
            if varReco["sousCategorie"].lower() == sousCategorie.lower()
        ]

    # Filtrage par public si le paramètre est présent dans l’URL
    if public:
        varRecommandations = [
            varReco for varReco in varRecommandations
            if varReco["public"].lower() == public.lower()
        ]

    # Retourne la liste finale après application des filtres
    return varRecommandations

@app.get("/api/recommandations/{id}")
def get_recommandation(id: int):
    """
    Route : GET /api/recommandations/{id}

    Rôle :
    Retourner une seule recommandation à partir de son identifiant.

    Exp:
    /api/recommandations/1
    """

    # Chargement des recommandations
    varRecommandations = charger_recommandations()

    # Recherche de la recommandation correspondant à l’id demandé
    for varReco in varRecommandations:
        if varReco["id"] == id:
            return varReco

    # Message retourné si aucune recommandation ne correspond à l’id
    return {"message": "Recommandation non trouvée"}
