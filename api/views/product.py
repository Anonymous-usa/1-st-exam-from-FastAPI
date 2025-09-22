from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
from api.schemas.product import ProductCreateSchema, ProductSchema
from api.models.product import Product
from auth.handlers import JWTBearer
from database import get_db
from .helpers import save_file  

product_router = APIRouter()

@product_router.get("/", response_model=List[ProductSchema], status_code=status.HTTP_200_OK, summary="Get all Products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@product_router.get("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK, summary="Get a Product by ID")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@product_router.post("/create", response_model=ProductSchema, status_code=status.HTTP_201_CREATED, summary="Create a new Product")
async def create_product(
    name: str = Form(...),  # Read name from form-data
    description: str = Form(...),  # Read description from form-data
    price: float = Form(...),  # Read price from form-data
    file: UploadFile = File(...),  # Handle image file upload
    db: Session = Depends(get_db),
):
    # Save the image file and get the filename
    image_result = await save_file(file)
    if image_result["status"] != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error saving image: {image_result['error']}")
    
    # Create the product object
    new_product = Product(
        name=name,
        description=description,
        price=price,
        image=image_result["message"],  # Store the image filename
    )
    
    # Save the product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@product_router.put("/update/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK, summary="Update a Product by ID", dependencies=[Depends(JWTBearer())])
async def update_product(
    product_id: int,
    name: str = Form(...),  # Get name from form data
    description: str = Form(...),  # Get description from form data
    price: float = Form(...),  # Get price from form data
    db: Session = Depends(get_db),
    file: UploadFile = File(None)  # Image file is optional
):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # If there's an image file, save it and update the image field
    if file:
        image_result = await save_file(file)
        if image_result["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error saving image: {image_result['error']}")
        product.image = image_result["message"]  # Update image filename
    
    # Update other fields (name, description, price)
    product.name = name
    product.description = description
    product.price = price
    
    # Commit changes to the database
    db.commit()
    db.refresh(product)
    
    return product

@product_router.delete("/delete/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Product by ID", dependencies=[Depends(JWTBearer())])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return None

@product_router.get("/search/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK, summary="Search Products by name")
def search_products(name: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.ilike(f"%{name}%")).all()
    return products

@product_router.get("/filter/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK, summary="Filter Products by price range")
def filter_products(min_price: float = 0, max_price: float = 10000, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.price.between(min_price, max_price)).all()
    return products
