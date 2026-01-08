from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class GoldPurchase(Base):
    __tablename__ = "gold_purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    amount = Column(Float)
    gold_price_per_gram = Column(Float)
    gold_grams = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
