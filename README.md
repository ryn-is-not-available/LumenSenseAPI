# LumenSense 🧠 
**The AI Triage Engine for B2B Sales**

Stop letting your AI chatbot fumble $50k enterprise leads. LumenSense is a headless AI routing layer that sits between your users and your chatbot. It passively analyzes chat histories in real-time to detect high-intent buyers, instantly routing them to your human sales team via Slack before they bounce.

## 🚀 The Problem We Solve
AI bots are great at deflecting tier-1 support tickets, but terrible at closing enterprise deals. When a VP of Engineering asks for 150 seats and SOC-2 compliance, they shouldn't get a generic FAQ link. LumenSense intercepts that conversation, analyzes the psychological subtext, and pages a human. 

**Zero spam for the sales team. They only get pinged when a whale is in the net.**

## ⚙️ How It Works


1. **Passive Listening:** Send the user's full chat history to the LumenSense `/api/analyze` endpoint.
2. **Psychological Profiling:** Powered by Llama-3.3-70b (via Groq for sub-second latency), it extracts the user's *Persona*, *Core Concern*, and *Buying Intent (0-100%)*.
3. **Zero-Latency Routing:** LumenSense instantly returns a `200 OK` to your bot so the user experiences zero lag. If Buying Intent hits the threshold (e.g., 80%+), it silently fires a rich UI card to a Slack channel in the background with a "Take Over Chat" button.

## 🛠️ Tech Stack
* **Framework:** FastAPI (with BackgroundTasks for zero-latency execution)
* **LLM Engine:** Groq API (Llama-3)
* **Security:** API Key Header Injection
* **Data Validation:** Pydantic
* **Integrations:** Slack Webhooks (Block Kit)

## 💻 Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ryn-is-not-available/LumenSenseAPI.git](https://github.com/ryn-is-not-available/LumenSenseAPI.git)
   cd LumenSenseAPI



2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up your environment variables:**
Create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
LUMENSENSE_API_KEY=ls_beta_your_custom_secret_key

```


4. **Run the server:**
```bash
uvicorn main:app --reload

```


The API will be live at `http://127.0.0.1:8000`.

## 📡 API Usage

**Endpoint:** `POST /api/analyze`

**Headers Required:**

* `x-api-key`: `your_custom_secret_key`

**Request Body (Context-Aware Array):**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hi team. We are migrating off your competitor and looking to deploy 150 enterprise licenses."
    },
    {
      "role": "bot",
      "content": "That is great! Are there any specific features you need for your deployment?"
    },
    {
      "role": "user",
      "content": "Yes, it must support SAML SSO by the end of the month."
    }
  ]
}

```

**Response (and simultaneous Background Slack Ping):**

```json
{
  "persona": "Technical Decision Maker",
  "sentiment": "urgent",
  "buying_intent_score": 95,
  "main_concern": "Enterprise security, fast migration, and SAML SSO",
  "tactical_advice": "Route immediately to an Account Executive. Emphasize security compliance and fast onboarding.",
  "is_hot_lead": true
}

```

## ☁️ Deployment

This project is fully ready to be deployed on Render, Heroku, or Railway. Simply connect your GitHub repo, set your Build Command to `pip install -r requirements.txt`, your Start Command to `uvicorn main:app --host 0.0.0.0 --port $PORT`, and paste your environment variables into the platform's dashboard.

---

*Built by Massek Rayen - [LinkedIn*](https://www.linkedin.com/in/rayen-messek-206322249/)

```