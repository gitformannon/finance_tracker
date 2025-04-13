from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.auth import router as auth_router
from api.cards import router as card_router
from api.transactions import router as transactions_router
from database.session import engine
from models import Base
from scripts.seed_data import seed
from telegram import Update
from telegram_bot.telegram_bot import application  # Make sure this points to your Application instance
import os
import logging

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

    if os.getenv("SEED_ENABLED", "false").lower() == "true":
        await seed()

    # Initialize Telegram bot application
    await application.initialize()
    logging.info("Telegram Application initialized.")

@app.get("/webhook")
def webhook_status():
    return {"message": "Webhook endpoint is alive, but POST is required."}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logging.exception("Error handling Telegram webhook")
        return JSONResponse(status_code=500, content={"error": str(e)})