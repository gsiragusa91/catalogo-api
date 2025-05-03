from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from collections import OrderedDict
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de entrada (sin ID)
class Product(BaseModel):
    title: str = Field(..., example="Auriculares Bluetooth")
    description: str = Field(..., example="Auriculares con cancelación de ruido")
    price: float = Field(..., gt=0, example=59.99)
    stock: int = Field(..., ge=0, example=100)
    category: str = Field(..., example="Electrónica")
    image_url: str = Field(..., example="https://via.placeholder.com/150")

# Base de datos en memoria
products = [
    {
        "id": 1,
        "title": "Auriculares Bluetooth",
        "description": "Auriculares inalámbricos con cancelación de ruido",
        "price": 59.99,
        "stock": 120,
        "category": "Electrónica",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 2,
        "title": "Zapatillas Running",
        "description": "Zapatillas livianas para correr largas distancias",
        "price": 89.99,
        "stock": 85,
        "category": "Deportes",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 3,
        "title": "Mochila Deportiva",
        "description": "Mochila resistente para actividades deportivas",
        "price": 45.00,
        "stock": 150,
        "category": "Accesorios",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 4,
        "title": "Mochila Escolar",
        "description": "Mochila liviana ideal para estudiantes",
        "price": 40.00,
        "stock": 80,
        "category": "Accesorios",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 5,
        "title": "Mochila Urbana",
        "description": "Diseño minimalista con espacio para notebook",
        "price": 55.00,
        "stock": 60,
        "category": "Accesorios",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 6,
        "title": "Smartwatch Pro",
        "description": "Reloj inteligente con GPS y monitoreo de salud",
        "price": 129.50,
        "stock": 60,
        "category": "Electrónica",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 7,
        "title": "Smartwatch Mini",
        "description": "Versión compacta de smartwatch con funciones básicas",
        "price": 79.90,
        "stock": 90,
        "category": "Electrónica",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 8,
        "title": "Camiseta Deportiva",
        "description": "Camiseta de secado rápido para entrenamiento",
        "price": 29.90,
        "stock": 200,
        "category": "Ropa",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 9,
        "title": "Camiseta Casual",
        "description": "Camiseta de algodón para uso diario",
        "price": 25.00,
        "stock": 170,
        "category": "Ropa",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "id": 10,
        "title": "Laptop Gamer",
        "description": "Laptop potente para gaming de alto nivel",
        "price": 1299.99,
        "stock": 20,
        "category": "Electrónica",
        "image_url": "https://via.placeholder.com/150"
    }
]

@app.get("/")
def root():
    return {"message": "Bienvenido al catálogo de productos"}

@app.get("/products")
def get_products():
    return products

@app.get("/products/search")
def search_products(name: Optional[str] = None, exact: Optional[bool] = False):
    if not name:
        raise HTTPException(status_code=422, detail="Parámetro 'name' requerido")
    if exact:
        return [p for p in products if name.lower() == p["title"].lower()]
    return [p for p in products if name.lower() in p["title"].lower()]

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.post("/products", status_code=201)
def create_product(product: Product):
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    ordered = OrderedDict()
    ordered["id"] = new_id
    ordered.update(product.dict())
    products.append(ordered)
    return ordered

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products[i] = OrderedDict(id=product_id, **updated_product.dict())
            return products[i]
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products.pop(i)
            return
    raise HTTPException(status_code=404, detail="Producto no encontrado")
