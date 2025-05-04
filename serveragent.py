import os
import requests
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from pydantic import Field

load_dotenv()

class ASI1Query(Model):
    query: str
    sender_address: str
    user_address: str

class ASI1Response(Model):
    response: str

class QuoteEmailRequest(Model):
    email: str
    summary: str
    user_address: str

EMAIL_AGENT_ADDRESS = "agent1qfategfwrdju2avwylfm6qj52xxayeyfgmrmukkk4f0v4kf6ygx2s6hdnda"

def get_asi1_response(query: str) -> str:
    api_key = os.getenv("ASI1_API_KEY")
    if not api_key:
        return "❌ ASI1 API key not found in environment variables."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = (
        "You are a proposal analyzer agent. Summarize the following RFQ. Extract:\n"
        "- I/O count\n"
        "- Delivery timeline\n"
        "- Payment terms\n"
        "- Communication protocols\n"
        "- Red flags if any (e.g., tight deadlines, post-payment risk)\n\n"
        "Text:\n"
        f"{query}"
    )

    data = {
        "model": "asi1-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful RFQ summarizer and risk assessor."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://api.asi1.ai/v1/chat/completions", json=data, headers=headers)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"ASI1 API Error: {res.status_code}"
    except Exception as e:
        return f"ASI1 API Error: {e}"

mainAgent = Agent(
    name="asi1_risk_summarizer",
    port=5068,
    endpoint="http://localhost:5068/submit",
    seed="asi1_risk_seed"
)

@mainAgent.on_event("startup")
async def on_start(ctx: Context):
    ctx.logger.info(f"✅ Server Agent ready at {ctx.agent.address}")

@mainAgent.on_message(model=ASI1Query)
async def handle_rfq(ctx: Context, sender: str, msg: ASI1Query):
    ctx.logger.info(f"📩 Received RFQ from {sender}")

    summary = get_asi1_response(msg.query)

    await ctx.send(msg.user_address, ASI1Response(response=summary))
    ctx.logger.info("📤 Sent summary to user")

    if EMAIL_AGENT_ADDRESS:
        await ctx.send(EMAIL_AGENT_ADDRESS, QuoteEmailRequest(
            email="jessicasanctis12@gmail.com",
            summary=summary,
            user_address=msg.user_address
        ))
        ctx.logger.info("✉️ Sent summary to Email Agent")

if __name__ == "__main__":
    mainAgent.run()
