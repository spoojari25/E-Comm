# import pytest
# import requests
from fastapi.testclient import TestClient
from app.main import app  # assuming your FastAPI app instance is named app

# Create a TestClient instance to interact with the FastAPI app
client = TestClient(app)



def test_create_product():
    # Define the product data to be sent in the request body
    product_data = {
        "title": "Test Product",
        "description": "Test Description",
        "price": 10.0
    }

    # Send a POST request to the /products endpoint
    response = client.post("/products", json=product_data)

    # Verify that the request was successful (status code 201 CREATED)
    assert response.status_code == 201

    # Verify that the response contains the created product data
    created_product = response.json()
    assert created_product["title"] == product_data["title"]
    assert created_product["description"] == product_data["description"]
    assert created_product["price"] == product_data["price"]


def test_get_products():
    # Send a GET request to the /products endpoint
    response = client.get("/products")

    # Verify that the request was successful (status code 200 OK)
    assert response.status_code == 200

    # Verify that the response contains a list of products
    products = response.json()
    assert isinstance(products, list)


def test_get_product():
    # Send a GET request to the /products/{id} endpoint with a valid product ID
    response = client.get("/products/1")

    # Verify that the request was successful (status code 200 OK)
    assert response.status_code == 200

    # Verify that the response contains the product with the specified ID
    product = response.json()
    assert product["id"] == 1


def test_update_product():
    # Define the updated product data
    updated_product_data = {
        "title": "Updated Product",
        "description": "Updated Description",
        "price": 20.0
    }

    # Send a PUT request to the /products/{id} endpoint with a valid product ID
    response = client.put("/products/1", json=updated_product_data)

    # Verify that the request was successful (status code 200 OK)
    assert response.status_code == 200

    # Verify that the response contains the updated product data
    updated_product = response.json()
    assert updated_product["title"] == updated_product_data["title"]
    assert updated_product["description"] == updated_product_data["description"]
    assert updated_product["price"] == updated_product_data["price"]


def test_delete_product():
    # Send a DELETE request to the /products/{id} endpoint with a valid product ID
    response = client.delete("/products/1")

    # Verify that the request was successful (status code 204 NO CONTENT)
    assert response.status_code == 204
