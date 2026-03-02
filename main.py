from fastapi import FastAPI, HTTPException, Security, Depends , BackgroundTasks
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List
from shared.analyzer import LumenSenseAnalyzer
import os
from dotenv import load_dotenv
import requests

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)  # For future API key security implementation

REAL_API_KEY = os.getenv("LUMENSENSE_API_KEY")

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == REAL_API_KEY:
        return api_key_header
    
    raise HTTPException(status_code=401, detail="Invalid API Key, Access Denied")
# 1. Initialize the App (Updated description for the new business model!)
app = FastAPI(title="LumenSense API", description="AI Triage Engine for B2B Sales")

# 2. Define the expected input (Pydantic makes sure the user sends the right data)
class Message(BaseModel):
    role: str  # "user" or "system"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]  # We expect a list of messages to better mimic real chat interactions

# 3. Initialize the Analyzer 
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
async def analyze_chat(
    request: ChatRequest, 
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    
    # 1. VALIDATION: Check if the messages list is empty
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages array cannot be empty")
    
    try:
        # 2. STITCHING: Turn the array of messages into a single readable transcript
        transcript = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in request.messages])
        
        # 3. ANALYSIS: Pass the compiled transcript to the LumenSenseAnalyzer
        result = analyzer.analyze(transcript)
        
        # 4. Wake up the sales team if it's a whale (NOW IN THE BACKGROUND ⚡)
        if result.get("is_hot_lead"):
            # We hand the Slack ping to FastAPI's background worker so we can hang up instantly!
            background_tasks.add_task(
                fire_slack_alert,
                profile=result.get("profile", {}),
                insights=result.get("insights", {}),
                original_text=transcript  
            )
            
        return result
        
    except Exception as e:
        # 5. FALLBACK: Never crash a client's chatbot. Fail gracefully.
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
    except Exception as e:
        # Failing gracefully is crucial for production!
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))