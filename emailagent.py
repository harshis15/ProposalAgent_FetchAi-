import smtplib
from email.mime.text import MIMEText
from uagents import Agent, Context, Model

class ASI1Response(Model):
    response: str

class QuoteEmailRequest(Model):
    email: str
    summary: str
    user_address: str

proposal_agent = Agent(
    name="proposal_generator",
    port=5072,
    endpoint="http://localhost:5072/submit",
    seed="proposal_gen_seed"
)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "jessicasanctis12@gmail.com"
EMAIL_PASSWORD = "sklt zpva sihn cwru"  # Consider using env vars

def send_quote_email(recipient_email, summary_text):
    subject = "Your Quote Summary from RFQ Analyzer"
    body = (
        "Hello,\n\n"
        "Please find below the summarized RFQ and estimated quote:\n\n"
        f"{summary_text}\n\n"
        "Estimated Price: $1500 USD\n"
        f"Quote ID: Q-{hash(summary_text) % 10000}\n\n"
        "Thank you,\n"
        "ASI1 Quote Bot"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Email failed: {e}"

@proposal_agent.on_event("startup")
async def on_start(ctx: Context):
    ctx.logger.info(f"✅ Email Agent ready at {ctx.agent.address}")

@proposal_agent.on_message(model=QuoteEmailRequest)
async def handle_summary(ctx: Context, sender: str, msg: QuoteEmailRequest):
    ctx.logger.info(f"📨 Received summary to send to {msg.email}")
    result = send_quote_email(msg.email, msg.summary)
    ctx.logger.info(result)

    await ctx.send(msg.user_address, ASI1Response(response=result))

if __name__ == "__main__":
    proposal_agent.run()
