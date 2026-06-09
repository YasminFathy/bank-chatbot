"""
deploy.py
Deploys the bank transaction chatbot to Vertex AI Agent Engine.

Before running this script, follow the production switching steps in README.md:
  - Set GOOGLE_GENAI_USE_VERTEXAI=TRUE in .env
  - Set GOOGLE_CLOUD_PROJECT in .env
  - Set GOOGLE_CLOUD_LOCATION in .env
  - Update model="gemini-2.0-flash" in bank_agent/agent.py

See: README.md — "Switching to production (Vertex AI)" section
"""

import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
from bank_agent import agent

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west2")
BUCKET = f"gs://{PROJECT_ID}-agent-staging"
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")

if not PROJECT_ID:
    print("ERROR: GOOGLE_CLOUD_PROJECT not set in .env")
    raise SystemExit(1)

print(f"Deploying to project: {PROJECT_ID}, location: {LOCATION}")
print(f"Creating staging bucket: {BUCKET}")

# Create the staging bucket if it doesn't exist
os.system(
    f"gcloud storage buckets create {BUCKET} --project={PROJECT_ID} --location={LOCATION} 2>/dev/null || echo 'Bucket already exists'"
)

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=BUCKET)

remote = agent_engines.create(
    agent_engines.AdkApp(agent=agent),
    requirements=[
        "google-adk[extensions]>=1.0.0",
        "google-cloud-aiplatform[agent_engines,reasoningengine]>=1.71.0",
        "openai>=1.30.0",
        "python-dotenv>=1.0.0",
        "cloudpickle>=3.1.2",
        "litellm>=1.75.5",
        "pydantic>=2.12.5",
    ],
    extra_packages=[
        "./bank_agent"
    ],  # budles local bank_agent folder into the deployment package so the remote environment can find it.
    env_vars={
        "OPENAI_API_KEY": OPENAI_KEY,
    },
    display_name="bank-transaction-chatbot",
    description="Customer-facing bank transaction chatbot PoC",
)

print(f"Deployed successfully!")
print(f"Resource: {remote.resource_name}")
