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
