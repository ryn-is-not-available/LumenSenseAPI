# LumenSense 🧠 | AI Lead Triage & Sentiment Routing

![LumenSense Architecture](images/placeholder-for-banner.png)

**LumenSense** is a headless "Psychological Intelligence" microservice designed for B2B revenue teams. It sits between your users and your AI chatbot, analyzing conversation logs in real-time to detect high-value enterprise leads and at-risk customers, instantly routing them to human representatives before deals are lost.

Stop letting tone-deaf AI agents handle your most important accounts. Let the bots handle the tier-1 support noise, and route the whales directly to your sales floor.

## 🎯 The Business Value

* **Enterprise Lead Routing (Triage):** Automatically identifies high-intent buyers based on behavioral subtext and specific keywords (e.g., "SOC-2", "Enterprise SLA", "50+ seats").
* **Churn De-escalation:** Detects rising frustration in customer support chats and triggers immediate human handoffs before a cancellation occurs.
* **Frictionless Handoff:** Integrates seamlessly with Slack, Microsoft Teams, and standard CRM webhooks to ping Account Executives the exact second a hot lead is detected.
* **Sub-Second Latency:** Powered by Llama-3.3-70b via the Groq API, ensuring zero disruption to your existing chatbot's response times.

---

## ⚙️ How It Works

LumenSense operates as a passive API layer. It does not replace your chatbot; it supercharges it.

1. **Ingest:** Your system (Website Bot, Telegram, Zendesk) sends the raw customer message to the LumenSense `/analyze` endpoint.
2. **Analyze:** The LLM engine profiles the user, extracting *Persona*, *Sentiment*, and *Buying Intent (0-100%)*.
3. **Action:** * If `Buying Intent < 70%`: LumenSense returns standard metadata, and your AI continues the conversation. Cost: fractions of a cent.
   * If `Buying Intent ≥ 70%`: LumenSense fires a rich-text webhook to your Sales Team's Slack channel with a "Tactical Dossier" and a one-click button to take over the chat.

---

## 📸 Live Demo: The Handoff in Action

*Left: A frustrated enterprise buyer talking to a standard chatbot. Right: The instant Slack alert sent to the human Sales Team.*

![Split Screen Demo](images/demo-placeholder.gif) 
*(Note: Replace with your actual split-screen GIF/Video once recorded)*

---

## 🏗️ Technical Architecture

LumenSense is built for scale and ease of integration by modern engineering teams.

* **Core Framework:** FastAPI (Python)
* **Inference Engine:** Groq API (Llama-3.3-70b-versatile)
* **Data Validation:** Pydantic
* **Deployment:** Serverless / Containerized (Render)
* **Alerting:** Native Webhook payloads (Slack Block Kit compatible)

---

## 🔌 API Integration Quickstart

Integrating LumenSense requires just a single HTTP POST request. 

**Endpoint:** `POST /analyze`

**Request Body:**
```json
{
  "chat_log": "I like the platform, but my CTO won't approve the budget unless we can confirm you have on-premise hosting options and SOC-2 compliance."
}

```

**Response Payload:**

```json
{
  "profile": {
    "persona": "Technical Decision Maker",
    "sentiment": "Cautious but interested",
    "buying_intent": 85
  },
  "insights": {
    "main_concern": "Security and compliance standards",
    "tactical_advice": "Bypass the standard pitch. Immediately provide SOC-2 documentation and route to a technical Account Executive."
  },
  "is_hot_lead": true
}

```

*(Note: When `is_hot_lead` returns `true`, the LumenSense backend can be configured to automatically dispatch a webhook to your CRM or Slack workspace).*

---

## 💻 Local Development

1. **Clone the repository:**
```bash
git clone [https://github.com/ryn-is-not-available/LumenSenseAPI.git](https://github.com/ryn-is-not-available/LumenSenseAPI.git)
cd LumenSenseAPI

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Environment Setup:**
Create a `.env` file and add your credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
SLACK_WEBHOOK_URL=your_optional_slack_url_here

```


4. **Run the server:**
```bash
uvicorn main:app --reload

```


*Interactive Swagger Documentation is automatically generated at `http://127.0.0.1:8000/docs*`
