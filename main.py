from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def charger_recommandations():
    with open("recommandations.json", "r", encoding="utf-8") as fichier:
        return json.load(fichier)

@app.get("/")
def accueil():
    return {"message": "API Recommandations de santé"}

@app.get("/api/recommandations")
def get_recommandations(categorie: str = None, sousCategorie: str = None, public: str = None):
    varRecommandations = charger_recommandations()

    if categorie:
        varRecommandations = [
            varReco for varReco in varRecommandations
            if varReco["categorie"].lower() == categorie.lower()
        ]

    if sousCategorie:
        varRecommandations = [
            varReco for varReco in varRecommandations
            if varReco["sousCategorie"].lower() == sousCategorie.lower()
        ]

    if public:
        varRecommandations = [
            varReco for varReco in varRecommandations
            if varReco["public"].lower() == public.lower()
        ]

    return varRecommandations

@app.get("/api/recommandations/{id}")
def get_recommandation(id: int):
    varRecommandations = charger_recommandations()

    for varReco in varRecommandations:
        if varReco["id"] == id:
            return varReco

    return {"message": "Recommandation non trouvée"}
