from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API online y funcionando desde Vercel!"}

handler = Mangum(app)
