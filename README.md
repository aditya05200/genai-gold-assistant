# 🟡 Simplify Money – GenAI Gold Assistant

A **Gen AI–powered backend service** that emulates a digital gold investment workflow.  
This system leverages Large Language Models (LLMs) for conversational intent handling, integrates live market data for pricing, and manages persistent investment records.

---

## 🚀 Features

- 🤖 **GenAI Chat Assistant**: Provides investment insights and classifies user intent (`GOLD`, `BUY`, `OTHER`).
- 💰 **Digital Gold Purchase API**: Real-time calculation of gold grams based on current market rates.
- 📈 **Live Gold Price Integration**: Integration with **GoldAPI.io** with a robust fallback mechanism.
- 🗄️ **Database Persistence**: Securely stores purchase records using SQLAlchemy ORM.
- ☁️ **Cloud Ready**: Configured for seamless deployment on Render, Railway, or Heroku.

---

## 🧠 Tech Stack

| Layer            | Technology                  |
| ---------------- | --------------------------- |
| **Backend**      | FastAPI (Python 3.10+)      |
| **GenAI**        | OpenAI GPT-4o-mini          |
| **Database**     | PostgreSQL / MySQL (SQLAlchemy) |
| **Pricing API**  | GoldAPI.io                  |
| **Infrastructure** | Docker-ready / Render / Railway |

---

## 📁 Project Structure

```text
genai-gold-assistant/
├── app.py                 # FastAPI routes and logic
├── database.py            # DB connection & session management
├── models.py              # SQLAlchemy database schemas
├── gold_price_service.py  # Live gold price fetching + fallback
├── prompts.py             # LLM system prompts & templates
├── requirements.txt       # Project dependencies
├── Procfile               # Deployment command for PaaS
└── README.md              # Documentation
```

## ⚙️ Setup & Installation

### 1. Environment Variables
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key
GOLDAPI_KEY=your_goldapi_key
DATABASE_URL=postgresql://user:password@host:port/dbname
```
### 2. Local Development

# Create and activate virtual environment

```python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app:app --reload
The API will be available at http://127.0.0.1:8000.
```

## 🧪 API Documentation
🔹 Chat Assistant
POST ```/chat```

Purpose: Handles natural language queries about gold.

Request: ```{"user_id": "U101", "message": "Why should I buy gold?"}```

Response: ```{"intent": "GOLD", "reply": "..."}```

🔹 Purchase Execution
POST ```/purchase```

Purpose: Executes a simulated gold buy order.

Request: ```{"user_id": "U101", "amount": 5000}```

Response: ```{"status": "SUCCESS", "gold_grams": 0.82, ...}```
