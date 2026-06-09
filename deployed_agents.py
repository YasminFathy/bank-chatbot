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


vertexai.init(
    project='gen-lang-client-0019475937',
    location='europe-west2'
)

agents = list(agent_engines.list())
print(f"Total deployed agents: {len(agents)}")
for a in agents:
    print(f"---")
    print(f"Name:     {a.display_name}")
    print(f"Resource: {a.resource_name}")
    print(f"Created:  {a.create_time}")


remote = agent_engines.get(
    'projects/297787477567/locations/europe-west2/reasoningEngines/7202082636909510656'
)

print(f"Agent found: {remote.display_name}")

# Create session and print it
session = remote.create_session(user_id='demo')
print(f"Session created: {session}")
print("---")

# Count chunks
chunks = list(remote.stream_query(
    user_id='demo',
    session_id=session['id'],
    message='What is my current balance?'
))

print(f"Total chunks received: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk}")