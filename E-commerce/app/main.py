from fastapi import FastAPI
from api.products import router as product_router
# from models.connection import get_connection
# conn = get_connection()
# print(conn)
app=FastAPI()

app.include_router(product_router)
