# backend/app/bot.py
from typing import Dict

# very small in-memory context for demonstration only
_user_context: Dict[str, list] = {}

def bot_response(user_email: str, text: str) -> str:
    # store context
    _user_context.setdefault(user_email, []).append(text)
    t = text.lower().strip()
    if "hi" in t or "hello" in t:
        return "Hello! I'm WhatsEase bot. How can I help?"
    if "help" in t:
        return "I can answer simple questions: ask about features, or say 'history' to see last messages."
    if "history" in t:
        last = _user_context.get(user_email, [])[-5:]
        return "Your recent messages: " + " | ".join(last)
    # default fallback
    return "Sorry, I didn't understand. Try 'help'."
