from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import category, product
from app.routes import auth, stock, dashboard
from app.database import Base, engine
from app.routes.audit import router as audit_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "https://crateline.netlify.app",
        "https://*.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(stock.router)
app.include_router(dashboard.router)
app.include_router(audit_router)