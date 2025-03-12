from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from app.lotes_process import optimizar_lotes, optimizar_lotes_csv
import pandas as pd

app = FastAPI()

class OptimizacionParams(BaseModel):
    peso_minimo: float
    peso_maximo: float
    auRec_min: float
    auRec_max: float

@app.get("/")
def home():
    return {"message": "Bienvenido a la API de procesamiento de datos"}


@app.post("/best_group")
async def best_group(
    file: UploadFile = File(...),
    peso_minimo: float = Form(...),
    peso_maximo: float = Form(...),
    auRec_min: float = Form(...),
    auRec_max: float = Form(...)):
    try:
        if file.content_type != "text/csv":
            return {"error": "El archivo debe ser un CSV."}
        
        df_selected = pd.read_csv(file.file)

        result = optimizar_lotes(df_selected, peso_minimo, peso_maximo, auRec_min, auRec_max)

        return result

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
    

@app.post("/best_group_csv")
async def best_group():
    try:
        result = optimizar_lotes_csv(200, 210, 0.86, 0.92)

        return result

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}