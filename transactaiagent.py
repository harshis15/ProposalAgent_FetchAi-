# transactai_agent.py
from uagents import Agent, Context, Model
from pydantic import Field
from datetime import datetime
from uuid import uuid4

# ----------- Models -----------
class TransactionRequest(Model):
    email: str
    summary: str

class TransactionStatus(Model):
    status: str

# ----------- Agent Setup -----------
transact_agent = Agent(
    name="transact_ai_agent",
    port=5073,
    endpoint="http://localhost:5073/submit",
    seed="transactai_seed"
)

# ----------- Startup Event -----------
@transact_agent.on_event("startup")
async def on_start(ctx: Context):
    ctx.logger.info(f"💳 TransactAI Agent is live!")
    ctx.logger.info(f"📬 Agent address: {ctx.agent.address}")
    #ctx.logger.info(f"🌐 Endpoint: {transact_agent.endpoint}")

# ----------- Transaction Handler -----------
@transact_agent.on_message(model=TransactionRequest)
async def handle_transaction(ctx: Context, sender: str, msg: TransactionRequest):
    ctx.logger.info(f"💼 Transaction initiated for: {msg.email}")

    # Simulate or implement real transaction logic
    transaction_id = f"TXN-{hash(msg.summary + msg.email) % 100000}"
    status = f"✅ Transaction successful. ID: {transaction_id} at {datetime.utcnow()}"

    ctx.logger.info(status)

    await ctx.send(sender, TransactionStatus(status=status))

# ----------- Run Agent -----------
if __name__ == "__main__":
    transact_agent.run()
