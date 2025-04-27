from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# Modelo de producto
class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str


# Base de datos simulada
products = [{
    "id": 1,
    "title": "Auriculares Bluetooth",
    "description": "Auriculares inalámbricos con cancelación de ruido",
    "price": 59.99,
    "stock": 120,
    "category": "Electronics",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 2,
    "title": "Zapatillas Running",
    "description": "Zapatillas livianas para correr largas distancias",
    "price": 89.99,
    "stock": 85,
    "category": "Sportswear",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 3,
    "title": "Mochila Deportiva",
    "description": "Mochila resistente para actividades deportivas",
    "price": 45.00,
    "stock": 150,
    "category": "Accessories",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 4,
    "title": "Mochila Escolar",
    "description": "Mochila liviana ideal para estudiantes",
    "price": 40.00,
    "stock": 80,
    "category": "Accessories",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 5,
    "title": "Smartwatch Pro",
    "description": "Reloj inteligente con GPS y monitoreo de salud",
    "price": 129.50,
    "stock": 60,
    "category": "Electronics",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 6,
    "title": "Smartwatch Mini",
    "description": "Versión compacta de smartwatch con funciones básicas",
    "price": 79.90,
    "stock": 90,
    "category": "Electronics",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 7,
    "title": "Camiseta Deportiva",
    "description": "Camiseta de secado rápido para entrenamiento",
    "price": 29.90,
    "stock": 200,
    "category": "Sportswear",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 8,
    "title": "Camiseta Casual",
    "description": "Camiseta de algodón para uso diario",
    "price": 25.00,
    "stock": 170,
    "category": "Clothing",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 9,
    "title": "Laptop Pro",
    "description": "Laptop de alto rendimiento para profesionales",
    "price": 999.99,
    "stock": 30,
    "category": "Electronics",
    "image_url": "https://via.placeholder.com/150"
}, {
    "id": 10,
    "title": "Laptop Gamer",
    "description": "Laptop potente para gaming de alto nivel",
    "price": 1299.99,
    "stock": 20,
    "category": "Electronics",
    "image_url": "https://via.placeholder.com/150"
}]

# Rutas de la API


@app.get("/")
def root():
    return {"message": "Bienvenido al Catálogo de Productos"}


@app.get("/products", response_model=List[Product])
def get_products():
    return products


@app.get("/products/search", response_model=List[Product])
def search_products(name: Optional[str] = None, exact: Optional[bool] = False):
    if not name:
        return {"error": "Debes proporcionar un parámetro de búsqueda 'name'."}

    if exact:
        filtered = [p for p in products if name.lower() == p["title"].lower()]
    else:
        filtered = [p for p in products if name.lower() in p["title"].lower()]

    if filtered:
        return filtered
    return []


@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return product
    return {"error": "Producto no encontrado"}
