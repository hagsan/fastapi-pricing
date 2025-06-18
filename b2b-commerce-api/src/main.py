from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.database import engine
from src.database import models
from src.routers import pricing_router, cart_router
import uvicorn

# Create the FastAPI app
app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pricing_router.router)
app.include_router(cart_router.router)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the B2B Commerce API"}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')