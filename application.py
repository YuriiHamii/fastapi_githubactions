from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: Union[float, None] = None
    tags: list[str] = []
  # tax: float = 10.5                       # Default Values

products = {
    "1": {"name": "CocaCola", "price": 1.2},
    "2": {"name": "PepsiCola", "description": "Orange", "price": 1.5, "tax": 0.2},
    "3": {"name": "Fanta", "description": None, "price": 1.8, "tax": 0.3, "tags": []},
}


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: str):
    return products[product_id]


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product):
    update_product_encoded = jsonable_encoder(product)
    products[product_id] = update_product_encoded
    return update_product_encoded


@app.get("/products")
async def get_products():
    return products

@app.post("/products", status_code=201)
async def add_products(product: Product):
    products.append(product)
    return product

@app.patch("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product):
    stored_product_data = products[product_id]
    stored_product_model = Product(**stored_product_data)
    update_data = product.dict(exclude_unset=True)
    updated_product = stored_product_model.copy(update=update_data)
    products[product_id] = jsonable_encoder(updated_product)
    return updated_product

    

if __name__ == "__main__":
    config = uvicorn.Config("application:app", host="fastapiproducts.eu-central-1.elasticbeanstalk.com", port=80, log_level="info")
    server = uvicorn.Server(config)
    server.run()
