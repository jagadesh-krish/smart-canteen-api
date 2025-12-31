from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.endpoints import customers, products, sales

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db()
    print("Database ready!")
    yield
    print("Shutting down...")

app = FastAPI(title="Smart Canteen API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(sales.router)

@app.get("/")
async def root():
    return {"message": "Smart Canteen API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
