from uagents import Agent, Context, Model
from pydantic import Field

class ASI1Query(Model):
    query: str
    sender_address: str
    user_address: str

class ASI1Response(Model):
    response: str

test_agent = Agent(name="test_agent", seed="test_agent_seed")

CLIENT_AGENT_ADDRESS = os.getenv("CLIENT_AGENT_ADDRESS")

rfq_text = """
Request for Quotation (RFQ)
From: AlphaTech Industries

Project Scope:
Design and supply of custom control panels for automation line.

Key Requirements:
- I/O Count: approx. 32
- Power: 24V DC
- Communication: Modbus RTU

Delivery: 2 weeks
Payment Terms: 100% post-installation

Regards,
John Doe
john.doe@alphatech.com
+91-9876543210
"""

@test_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("🚀 Sending RFQ to client agent...")
    await ctx.send(CLIENT_AGENT_ADDRESS, ASI1Query(
        query=rfq_text,
        sender_address=ctx.agent.address,
        user_address=ctx.agent.address
    ))

@test_agent.on_message(model=ASI1Response)
async def handle_response(ctx: Context, sender: str, msg: ASI1Response):
    print(f"\n📝 Got response from client:\n{msg.response}")

if __name__ == "__main__":
    test_agent.run()
