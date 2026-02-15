```markdown
# LumenSense 🧠⚡
> **The psychological intelligence layer for AI agents.**

LumenSense is an open-source, ultra-low-latency API that extracts real-time sentiment, buying intent, and tactical dossiers from raw chat logs. Built for speed using FastAPI and Llama-3 (via Groq), it allows your AI to pivot its strategy mid-conversation. Join the revolution in agentic EQ!

## 🚀 Features
* **Real-Time EQ:** Analyzes sentiment and assigns a specific user persona.
* **Conversion Tracking:** Calculates "Buying Intent" (0-100%).
* **Tactical Dossiers:** Identifies the user's main concern and provides the AI agent with specific advice on how to reply next.
* **Blazing Fast:** Powered by Llama-3.3-70b via the Groq API for sub-second inference times.
* **Developer Friendly:** Built on FastAPI with auto-generated Swagger UI documentation.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **LLM Engine:** Groq API (Llama-3.3-70b-versatile)
* **Data Validation:** Pydantic

---

## 💻 Local Quickstart

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/LumenSense-Core.git](https://github.com/YOUR_USERNAME/LumenSense-Core.git)
cd LumenSense-Core

```

### 2. Set up the environment

```bash
python -m venv .venv
# On Windows use: .venv\Scripts\activate
# On Mac/Linux use: source .venv/bin/activate
.venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Add your API Key

Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=gsk_your_api_key_here

```

### 4. Run the Server

```bash
uvicorn main:app --reload

```

*Your API is now running at `http://localhost:8000`.*
*View the interactive documentation at `http://localhost:8000/docs`.*

---

## 📡 API Usage

**Endpoint:** `/api/analyze`

**Method:** `POST`

### Request Body (JSON)

```json
{
  "chat_log": "I really like this tool, but $50 is just too expensive for my team right now. Do you have a startup discount?"
}

```

### Response Schema (JSON)

```json
{
  "analysis_id": "string",
  "profile": {
    "sentiment": "Hesitant",
    "buying_intent": 60,
    "persona": "Price-Sensitive Buyer"
  },
  "insights": {
    "main_concern": "Price is too high for their current budget",
    "tactical_advice": "Acknowledge the budget constraint and immediately offer the startup discount code."
  },
  "is_hot_lead": false
}

```

## 🤝 Contributing

Currently in private beta/early access. Feel free to open issues or submit PRs if you want to help build high-EQ agents!

```

```
