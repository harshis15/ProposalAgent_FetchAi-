import os
from dotenv import load_dotenv
from uagents import Agent, Context, Model

load_dotenv()

class QuoteEmailRequest(Model):
    email: str
    summary: str
    user_address: str

class ASI1Query(Model):
    query: str
    sender_address: str
    user_address: str

class ASI1Response(Model):
    response: str

clientAgent = Agent(
    name='asi1_user_agent',
    port=5070,
    endpoint='http://localhost:5070/submit',
    seed='asi1_user_seed'
)

# Replace with your actual server agent address
SERVER_AGENT_ADDRESS = "agent1qtnesq9kv9uwmw2842x9pga8rcal0wjajuz6x0n3yydtz9gcxcrss5s0ku3"

@clientAgent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f"🆔 Client Agent Address: {ctx.agent.address}")

@clientAgent.on_message(model=ASI1Response)
async def handle_response(ctx: Context, sender: str, msg: ASI1Response):
    print("\n🧾 Summarized Analysis:\n", msg.response)

if __name__ == "_main_":
    clientAgent.run()