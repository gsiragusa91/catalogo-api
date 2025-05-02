from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API funcionando correctamente en Vercel"}

handler = Mangum(app)
