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
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_893804-MLA52334469476_112022-F.webp"
    },
    {
        "id": 2,
        "title": "Zapatillas Running",
        "description": "Zapatillas livianas para correr largas distancias",
        "price": 89.99,
        "stock": 85,
        "category": "Deportes",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_995491-MLA71637919512_092023-F.webp"
    },
    {
        "id": 3,
        "title": "Mochila Deportiva",
        "description": "Mochila resistente para actividades deportivas",
        "price": 45.00,
        "stock": 150,
        "category": "Accesorios",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_789732-MLA70119474986_062023-F.webp"
    },
    {
        "id": 4,
        "title": "Mochila Escolar",
        "description": "Mochila liviana ideal para estudiantes",
        "price": 40.00,
        "stock": 80,
        "category": "Accesorios",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_969790-MLA75113134435_032024-F.webp"
    },
    {
        "id": 5,
        "title": "Smartwatch Pro",
        "description": "Reloj inteligente con GPS y monitoreo de salud",
        "price": 129.50,
        "stock": 60,
        "category": "Electrónica",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_849174-MLA48628251441_122021-F.webp"
    },
    {
        "id": 6,
        "title": "Smartwatch Mini",
        "description": "Versión compacta de smartwatch con funciones básicas",
        "price": 79.90,
        "stock": 90,
        "category": "Electrónica",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_963257-MLA75308518735_032024-F.webp"
    },
    {
        "id": 7,
        "title": "Camiseta Deportiva",
        "description": "Camiseta de secado rápido para entrenamiento",
        "price": 29.90,
        "stock": 200,
        "category": "Ropa",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_758838-MLA70139309851_062023-F.webp"
    },
    {
        "id": 8,
        "title": "Camiseta Casual",
        "description": "Camiseta de algodón para uso diario",
        "price": 25.00,
        "stock": 170,
        "category": "Ropa",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_944669-MLA72455999164_102023-F.webp"
    },
    {
        "id": 9,
        "title": "Laptop Pro",
        "description": "Laptop de alto rendimiento para profesionales",
        "price": 999.99,
        "stock": 30,
        "category": "Electrónica",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_853453-MLA70390214153_072023-F.webp"
    },
    {
        "id": 10,
        "title": "Laptop Gamer",
        "description": "Laptop potente para gaming de alto nivel",
        "price": 1299.99,
        "stock": 20,
        "category": "Electrónica",
        "image_url": "https://http2.mlstatic.com/D_NQ_NP_2X_982365-MLA75364010262_032024-F.webp"
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
