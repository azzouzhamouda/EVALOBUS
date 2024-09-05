from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def calculer_imc(poids, taille):
    try:
        imc = poids / (taille ** 2)
        return imc
    except ZeroDivisionError:
        return None

def evaluer_obesite(imc, sexe):
    if sexe.lower() == 'homme':
        if imc < 18.5:
            return "Poids insuffisant"
        elif 18.5 <= imc < 24.9:
            return "Poids normal"
        elif 25 <= imc < 29.9:
            return "Surpoids"
        elif 30 <= imc < 34.9:
            return "Obésité classe I"
        elif 35 <= imc < 39.9:
            return "Obésité classe II"
        else:
            return "Obésité classe III"
    elif sexe.lower() == 'femme':
        if imc < 18.5:
            return "Poids insuffisant"
        elif 18.5 <= imc < 24.9:
            return "Poids normal"
        elif 25 <= imc < 29.9:
            return "Surpoids"
        elif 30 <= imc < 34.9:
            return "Obésité classe I"
        elif 35 <= imc < 39.9:
            return "Obésité classe II"
        else:
            return "Obésité classe III"
    else:
        return "Sexe non reconnu. Veuillez entrer 'homme' ou 'femme'."

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def post_form(request: Request, poids: float = Form(...), taille: float = Form(...), sexe: str = Form(...)):
    imc = calculer_imc(poids, taille)
    if imc is None:
        resultat = "Erreur: La taille ne peut pas être zéro."
    else:
        evaluation = evaluer_obesite(imc, sexe)
        resultat = f"Votre IMC est: {imc:.2f}. Catégorie: {evaluation}"
    return templates.TemplateResponse("index.html", {"request": request, "resultat": resultat})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
