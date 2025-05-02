from fastapi import FastAPI
from typing import List, Optional

app = FastAPI()

products = [
    {"id": 1, "title": "Auriculares Bluetooth", "price": 59.99},
    {"id": 2, "title": "Zapatillas Running", "price": 89.99},
    {"id": 3, "title": "Mochila Deportiva", "price": 45.00},
    {"id": 4, "title": "Mochila Escolar", "price": 40.00},
]

@app.get("/")
def root():
    return {"message": "Bienvenido al catálogo"}

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return next((p for p in products if p["id"] == product_id), {"error": "Producto no encontrado"})

@app.get("/products/search")
def search_products(name: Optional[str] = None, exact: Optional[bool] = False):
    if not name:
        return []
    if exact:
        return [p for p in products if name.lower() == p["title"].lower()]
    return [p for p in products if name.lower() in p["title"].lower()]
