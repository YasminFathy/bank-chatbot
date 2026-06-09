"""
deployed_agents.py
Lists all deployed Vertex AI Agent Engine instances for this project.
Run with: python deployed_agents.py
"""

import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
import os

load_dotenv()


vertexai.init(project="gen-lang-client-0019475937", location="europe-west2")

agents = list(agent_engines.list())
print(f"Total deployed agents: {len(agents)}")
for a in agents:
    print(f"---")
    print(f"Name:     {a.display_name}")
    print(f"Resource: {a.resource_name}")
    print(f"Created:  {a.create_time}")


remote = agent_engines.get(
    "projects/297787477567/locations/europe-west2/reasoningEngines/7202082636909510656"
)

print(f"Agent found: {remote.display_name}")

# Create session and print it
session = remote.create_session(user_id="demo")
print(f"Session created: {session}")
print("---")

print(f"Q: What is my current balance?")
chunks = list(
    remote.stream_query(
        user_id="demo", session_id=session["id"], message="What is my current balance?"
    )
)

print(f"Total chunks received: {len(chunks)}")
for i, chunk in enumerate(chunks):
    if isinstance(chunk, dict):
        parts = chunk.get("content", {}).get("parts", [])
        for part in parts:
            if part.get("function_call"):
                print(
                    f"Chunk {i+1} [function_call]→ {part['function_call'].get('name')}()"
                )
            if part.get("function_response"):
                print(f"Chunk {i+1} [function_response] → tool result received")
            if part.get("text"):
                print(f"Chunk {i+1} [text] → {part['text']}")
