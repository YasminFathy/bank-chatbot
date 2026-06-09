from google.adk.agents import Agent

from bank_agent.tools import get_balance, get_transactions, lookup_merchant
from bank_agent.guardrails import input_guardrail, output_guardrail

SYSTEM_PROMPT = """Bank assistant for CUST-001 (demo).
Help with: balance, transactions, charge identification only.
Never discuss loans, investments, payments or give financial advice.
Only use data from tools. Be brief."""

'''
SYSTEM_PROMPT = """You are a helpful bank account assistant for demo bank customers.

You can ONLY help with:
- Checking account balance
- Viewing transaction history
- Identifying unfamiliar charges on a statement

You MUST NOT discuss or assist with:
- Loans, mortgages, or credit
- Investments, ISAs, pensions, or financial advice
- Payments, transfers, or any account changes
- Any topic unrelated to the customer's own transaction data

Rules:
- Use ONLY data returned by your tools. Never invent balances, amounts, or merchant names.
- Be concise and factual. Customers want quick answers.
- For anything out of scope, politely redirect: "For [topic], please call 0300 XXX XXXX or visit a branch."
- The authenticated customer for this session is CUST-001 (demo mode).
"""
'''

root_agent = Agent(
    name="bank_transaction_agent",
    # model="openai/gpt-4o-mini", # PoC / OpenAI
    model="openai/gemini-2.0-flash",  # production / Vertex AI
    description="Helps bank customers check balances, browse transactions, and identify charges.",
    instruction=SYSTEM_PROMPT,
    tools=[get_balance, get_transactions, lookup_merchant],
    before_tool_callback=input_guardrail,
    after_agent_callback=output_guardrail,
)
