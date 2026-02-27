from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from shared.analyzer import LumenSenseAnalyzer
import os
from dotenv import load_dotenv
import requests

# 1. Initialize the App (Updated description for the new business model!)
app = FastAPI(title="LumenSense API", description="AI Triage Engine for B2B Sales")

# 2. Define the expected input (Pydantic makes sure the user sends the right data)
class ChatRequest(BaseModel):
    chat_log: str

# 3. Instantiate our Chef
analyzer = LumenSenseAnalyzer()

# ==========================================
# 🚨 ENTERPRISE SLACK ROUTING LOGIC 🚨
# ==========================================
load_dotenv()  # Load environment variables from .env file
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def fire_slack_alert(profile, insights, original_text):
    """Fires an enterprise-grade Slack Block Kit UI alert."""
    if not SLACK_WEBHOOK_URL:
        print("⚠️ No Slack Webhook configured. Skipping alert.")
        return

    # Constructing a Slack UI Card using Block Kit
    slack_payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 High-Intent Lead Triage",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*👤 Persona:*\n{profile.get('persona', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*📈 Buying Intent:*\n{profile.get('buying_intent', 'N/A')}%"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🎯 Core Concern to Address:*\n{insights.get('main_concern', 'N/A')}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*💬 Raw Customer Input:*\n> \"_{original_text}_\""
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Take Over Chat ⚡",
                            "emoji": True
                        },
                        "style": "primary", 
                        "url": "https://your-crm-dashboard.com" # Where the sales rep goes
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=slack_payload)
        response.raise_for_status() 
        print("🔥 Enterprise Slack alert fired successfully!")
    except Exception as e:
        print(f"❌ Failed to send Slack alert: {e}")

# ==========================================
# 4. Define the Route
# ==========================================
@app.post("/api/analyze")
async def analyze_chat(request: ChatRequest):
    if not request.chat_log.strip():
        raise HTTPException(status_code=400, detail="chat_log cannot be empty")
    
    try:
        # Pass the data to the LumenSenseAnalyzer and get the insights
        result = analyzer.analyze(request.chat_log)
        
        # 🎯 NEW: Triage check! Wake up the human sales team if it's a whale.
        # (Assuming your analyzer returns a dictionary)
        if result.get("is_hot_lead"):
            fire_slack_alert(
                profile=result.get("profile", {}),
                insights=result.get("insights", {}),
                original_text=request.chat_log
            )
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))