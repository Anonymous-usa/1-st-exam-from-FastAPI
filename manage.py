import uvicorn

from fastapi import FastAPI

from database import BaseModel, engine
from auth.views import auth_router
from api.views.product import product_router
from api.views.cart import cart_router
from api.views.order import order_router



app = FastAPI(debug=True)

app.include_router(auth_router, prefix="/auth", tags=["Authentication endpoints"])
app.include_router(product_router, prefix="/products", tags=["Product endpoints"])
app.include_router(cart_router, prefix="/cart", tags=["Cart endpoints"])
app.include_router(order_router, prefix="/orders", tags=["Order endpoints"])


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=engine)
    uvicorn.run("manage:app", host= "localhost", port = 8000, reload = True)