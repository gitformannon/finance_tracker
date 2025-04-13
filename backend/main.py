from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router
from api.cards import router as card_router
from api.transactions import router as transactions_router
from database.session import engine
from models import Base
from seed_data import seed_transaction_types

app = FastAPI(title="Finance Tracker API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/backend/v1/fintracker/auth", tags=["Auth"])
app.include_router(card_router, prefix="/backend/v1/fintracker/cards", tags=["Cards"])
app.include_router(transactions_router, prefix="/backend/v1/fintracker/transactions", tags=["Transactions"])

# DB initialization (optional for dev)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)