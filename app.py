import os
import json
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, GoldPurchase
from prompts import GOLD_ASSISTANT_PROMPT
from gold_price_service import get_gold_price_per_gram

# Load environment variables
load_dotenv()

# Auto-create tables (Spring Boot ddl-auto equivalent)
Base.metadata.create_all(bind=engine)

# Configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="Simplify Money - Gen AI Gold Assistant",
    description="Gen AI powered assistant to emulate Covariate gold investment workflow",
    version="1.0"
)

# ---------- DB Dependency (Repository Equivalent) ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Request Models ----------

class ChatRequest(BaseModel):
    user_id: str
    message: str

class PurchaseRequest(BaseModel):
    user_id: str
    amount: float

# ---------- APIs ----------

@app.post("/chat")
def chat(request: ChatRequest):
    prompt = GOLD_ASSISTANT_PROMPT.format(user_input=request.message)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a finance-only AI assistant for Simplify Money. "
                    "Always respond in valid JSON only, without markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    text_response = response.choices[0].message.content.strip()
    text_response = text_response.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text_response)
    except Exception:
        return {
            "intent": "ERROR",
            "reply": text_response
        }


@app.post("/purchase")
def purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    gold_price_per_gram = get_gold_price_per_gram()
    gold_grams = round(request.amount / gold_price_per_gram, 2)

    # Save purchase in MySQL
    purchase_entry = GoldPurchase(
        user_id=request.user_id,
        amount=request.amount,
        gold_price_per_gram=gold_price_per_gram,
        gold_grams=gold_grams
    )

    db.add(purchase_entry)
    db.commit()
    db.refresh(purchase_entry)

    return {
        "status": "SUCCESS",
        "transaction_id": purchase_entry.id,
        "gold_price_per_gram": gold_price_per_gram,
        "message": (
            f"You have successfully purchased {gold_grams} grams "
            f"of digital gold via Simplify Money."
        )
    }
