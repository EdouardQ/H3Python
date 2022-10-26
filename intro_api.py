from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import mysql.connector


class Product(BaseModel):
    id: int
    name: str
    price: float


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Werlcome to this API"}


@app.get("/products", response_model=list[Product])
def readi_products():
    return getProducts()


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    data = getProduct(product_id)
    if isinstance(data, Product):
        return data
    return JSONResponse(status_code=404, content={"message": "The product was not found"})


# curl -X POST http://127.0.0.1:8000/products\?name\=stylo\&price\=3.80
@app.post("/products", response_model=Product)
def add_product(name: str, price: float):
    return insert_product(name, price)


def create_connexion():
    try:
        return mysql.connector.connect(user='root', password='root',
                                       host='127.0.0.1',
                                       database='shop')
    except mysql.connector.Error as err:
        print("Failed connecting to the database: {}".format(err))
        exit(1)


def getProducts():
    try:
        cnx = create_connexion()
        cursor = cnx.cursor()
        query = "SELECT * FROM product"

        cursor.execute(query)

        data = []
        for (id, name, price) in cursor.fetchall():
            data.append(Product(id=id, name=name, price=price))

        cursor.close()
        cnx.close()

        return data

    except mysql.connector.Error as err:
        print("Failed fetching database: {}".format(err))
        exit(1)


def getProduct(product_id: int):
    try:
        cnx = create_connexion()
        cursor = cnx.cursor()
        query = "SELECT * FROM product WHERE product.id = %s"

        cursor.execute(query, (product_id,))

        data = cursor.fetchall()
        if not data:
            return "invalid id"

        id, name, price = data[0]
        product = Product(id=id, name=name, price=price)

        cursor.close()
        cnx.close()

        return product

    except mysql.connector.Error as err:
        print("Failed fetching database: {}".format(err))
        exit(1)


def insert_product(name: str, price: float):
    try:
        cnx = create_connexion()
        cursor = cnx.cursor()
        query = "INSERT INTO product (name, price) VALUE (%s, %s)"

        cursor.execute(query, (name, price))
        cnx.commit()

        print(cursor.rowcount, "record inserted")
        product = Product(id=cursor.lastrowid, name=name, price=price)

        cursor.close()
        cnx.close()

        return product

    except mysql.connector.Error as err:
        print("Failed fetching database: {}".format(err))
        exit(1)
