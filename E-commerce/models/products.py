from pydantic import BaseModel


class Products(BaseModel):
    title:str
    description:str
    price:float