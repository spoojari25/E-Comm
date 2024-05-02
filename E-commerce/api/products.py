from fastapi import APIRouter,HTTPException,status
from models.products import Products
from models.connection import get_connection
router = APIRouter()
conn = get_connection()
cur=conn.cursor()


# Creating a product
@router.post("/products", response_model=Products, status_code=status.HTTP_201_CREATED)
def create_product(product: Products):
    try:
        cur.execute("""INSERT INTO products (title, description, price)
                        VALUES (%s, %s, %s) RETURNING * """,
                    (product.title, product.description, product.price))
        created_product = cur.fetchone()
        conn.commit()  
        if created_product:
            return created_product 
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



# Fetching all the products
@router.get("/products")
def get_products():
    try:
        cur.execute("""SELECT * from products""")
        products = cur.fetchall()
        return products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Fetching product based on specific id
@router.get("/products/{id}")
def get_product(id:int):
    try:
        cur.execute("""SELECT * from products where id = %s""",(str(id),))
        product = cur.fetchone()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product with id {id} does not exists")
        return product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# Update the product based on the specific id
@router.put("/products/{id}")
def update_product(id:int,products:Products):
    try:
        cur.execute("""UPDATE products SET title = %s,description=%s,price=%s WHERE id = %s RETURNING * """,
                    (products.title,products.description,products.price,str(id)))
        updated_product  = cur.fetchone()
        conn.commit()
        if not updated_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"product with id {id} does not exists")
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# delete the product based on the id
@router.delete("/products/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int):
    try:
        cur.execute(""" DELETE FROM products where id = %s RETURNING *  """,(str(id),))
        deleted_product = cur.fetchone()
        conn.commit()
        if not deleted_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"product with id {id} does not exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"data":"Product deleted successfully"}