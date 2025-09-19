import uvicorn

from fastapi import FastAPI

from database import BaseModel, engine
from auth.views import auth_router

app = FastAPI(debug=True)

app.include_router(auth_router, prefix="/auth", tags=["Authentication endpoints"])

if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=engine)
    uvicorn.run("manage:app", host= "localhost", port = 8000, reload = True)