import os
import json
import logging
from time import time
from typing import Dict, Any, Optional
from groq import Groq
from dotenv import load_dotenv

# 1. Setup Logging (Don't use print() in production!)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# 2. Define the System Prompt as a Constant (The "Brain")
SYSTEM_PROMPT = """
You are the core intelligence engine for LumenSense. 
Your goal is to analyze the provided chat log and extract "Psychological Subtext."

OUTPUT RULES:
- Return ONLY valid JSON.
- No markdown, no conversational filler.
- If the chat is empty or nonsense, return a neutral profile.

JSON SCHEMA:
{
  "analysis_id": "string",
  "profile": {
    "sentiment": "string",
    "buying_intent": number (0-100),
    "persona": "string"
  },
  "insights": {
    "main_concern": "string",
    "tactical_advice": "string"
  },
  "is_hot_lead": boolean
}
"""

class LumenSenseAnalyzer:
    def __init__(self):
        # Initialize client once
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def analyze(self, chat_log: str) -> Dict[str, Any]:
        """
        Analyzes a chat log and returns a structured psychological profile.
        """
        if not chat_log:
            return self._get_error_schema("Empty input provided")

        try:
            # 3. Proper Message Separation (Security)
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": chat_log}
                ],
                response_format={"type": "json_object"},
                temperature=0.1 # Lower is better for strict JSON
            )
            
            # Parse the response
            result = completion.choices[0].message.content
            return json.loads(result)

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return self._get_error_schema("AI Processing Error")

    def _get_error_schema(self, error_msg: str) -> Dict[str, Any]:
        """Returns a valid JSON structure even when things fail."""
        return {
            "analysis_id": "error",
            "profile": {
                "sentiment": "Error",
                "buying_intent": 0,
                "persona": "Unknown"
            },
            "insights": {
                "main_concern": error_msg,
                "tactical_advice": "Retry request"
            },
            "is_hot_lead": False
        }

