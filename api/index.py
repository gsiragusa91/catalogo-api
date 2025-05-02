from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from mangum import Mangum

app = FastAPI()

class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str

products = [
    {"id": 1, "title": "Auriculares Bluetooth", "description": "Auriculares inalámbricos", "price": 59.99, "stock": 120, "category": "Electronics", "image_url": "https://via.placeholder.com/150"},
    {"id": 2, "title": "Zapatillas Running", "description": "Zapatillas para correr", "price": 89.99, "stock": 85, "category": "Sportswear", "image_url": "https://via.placeholder.com/150"},
    {"id": 3, "title": "Mochila Deportiva", "description": "Mochila para deporte", "price": 45.00, "stock": 150, "category": "Accessories", "image_url": "https://via.placeholder.com/150"},
    {"id": 4, "title": "Mochila Escolar", "description": "Mochila para estudiantes", "price": 40.00, "stock": 80, "category": "Accessories", "image_url": "https://via.placeholder.com/150"},
    {"id": 5, "title": "Smartwatch Pro", "description": "Reloj inteligente", "price": 129.50, "stock": 60, "category": "Electronics", "image_url": "https://via.placeholder.com/150"},
    {"id": 6, "title": "Smartwatch Mini", "description": "Versión compacta", "price": 79.90, "stock": 90, "category": "Electronics", "image_url": "https://via.placeholder.com/150"},
    {"id": 7, "title": "Camiseta Deportiva", "description": "Camiseta para entrenar", "price": 29.90, "stock": 200, "category": "Sportswear", "image_url": "https://via.placeholder.com/150"},
    {"id": 8, "title": "Camiseta Casual", "description": "Camiseta de algodón", "price": 25.00, "stock": 170, "category": "Clothing", "image_url": "https://via.placeholder.com/150"},
    {"id": 9, "title": "Laptop Pro", "description": "Laptop profesional", "price": 999.99, "stock": 30, "category": "Electronics", "image_url": "https://via.placeholder.com/150"},
    {"id": 10, "title": "Laptop Gamer", "description": "Laptop para gaming", "price": 1299.99, "stock": 20, "category": "Electronics", "image_url": "https://via.placeholder.com/150"}
]

@app.get("/")
def root():
    return {"message": "Bienvenido al catálogo"}

@app.get("/products", response_model=List[Product])
def get_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    return product if product else {"error": "Producto no encontrado"}

@app.get("/products/search", response_model=List[Product])
def search_products(name: Optional[str] = None, exact: Optional[bool] = False):
    if not name:
        return []
    if exact:
        return [p for p in products if name.lower() == p["title"].lower()]
    return [p for p in products if name.lower() in p["title"].lower()]

# ✨ Adaptador para Vercel serverless
handler = Mangum(app)
