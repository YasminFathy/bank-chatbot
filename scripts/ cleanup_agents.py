"""
cleanup_agents.py
Deletes old and broken Vertex AI Agent Engine deployments.

Use this script when:
- A deployment failed due to wrong model string
- You have multiple agents and want to keep only the active one
- You want to free up resources and save GCP credits

The force=True parameter deletes all child sessions before
deleting the agent — required if the agent has been queried.

Run with: python scripts/cleanup_agents.py
"""

import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
import os

load_dotenv()

vertexai.init(project="gen-lang-client-0019475937", location="europe-west2")

# Delete the two broken ones — keep 7202082636909510656
to_delete = [
    "projects/297787477567/locations/europe-west2/reasoningEngines/6659398881811365888",
    "projects/297787477567/locations/europe-west2/reasoningEngines/4906372726857400320",
]

for resource in to_delete:
    try:
        agent = agent_engines.get(resource)
        agent.delete(force=True)
        print(f"Deleted: {resource.split('/')[-1]}")
    except Exception as e:
        print(f"Could not delete: {e}")

print("Done — run deployed_agents.py to confirm only one remains")
