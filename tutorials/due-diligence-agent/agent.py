import os

os.environ["AIXPLAIN_API_KEY"] = "<YOUR_API_KEY>"
os.environ["NUMEXPR_NUM_THREADS"] = "8"
os.environ["NUMEXPR_MAX_THREADS"] = "8"  

from aixplain.factories import AgentFactory, TeamAgentFactory
from aixplain.modules.agent.agent_task import AgentTask
import json
import logging
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Suppress logging
logging.getLogger().setLevel(logging.ERROR)

general_company_info = AgentTask(
    name="general_company_info",
    description="Use the CompanyIndex to find relevant general information about companies",
    expected_output="List of general information about the company"
)

financials_info = AgentTask(
    name="financials_info", 
    description="Find financial information about the company mentioned.",
    expected_output="List of financial information about the company"
)

online_market_landscape = AgentTask(
    name="online_market_landscape", 
    description="Find relevant information about the online market landscape related to the company",
    expected_output="Relevant information about the online market landscape."
)

online_reviews = AgentTask(
    name="online_reviews",
    description="Find online reviews about the company.",
    expected_output="Return review information about the company."
)

litigation_history = AgentTask(
    name="litigation_history",
    description="Retrieve all known legal issues, litigations, conflicts, or risk-related events.",
    expected_output="Summary and bullet points of all major events including dates,"
)

litigation_review = AgentTask(
    name="litigation_review",
    description="Review the legal issues to find details about the events and return risk associates.",
    expected_output="Sumamry of risk and details associated with the events",
    dependencies=[litigation_history]
)

knowledge_gathering_agent = AgentFactory.create(
    name="Knowledge Gathering Agent",
    description="Gathers geenral ifnormation, financials and online information about a company",
    instructions="""
What does the team know so far?
Combine information from the following:

General company info

Financial records


Online sentiment and reviews

Summarize the company's overall status across the above categories in under 300 words.
Use the website scraping tool for financial records, online market landscape, online reviews and general information""",
tasks=[general_company_info, financials_info, online_market_landscape, online_reviews],
tools=[
    AgentFactory.create_model_tool(model="6849dd3fd208307eba0cc122"), #Company Index
    AgentFactory.create_model_tool(model="65c51c556eb563350f6e1bb1"), #Google Search SERP
    AgentFactory.create_model_tool(model="66f423426eb563fa213a3531"), #Scrape Website Tool
],
)

litigation_agent = AgentFactory.create(
    name="Legal Litigation Agent",
    description="Finds legal litigation information about a company",
    instructions="""
Given the company name below, retrieve all known legal issues, litigations, conflicts, or risk-related events.
Summarize them in a short paragraph, then provide a bulleted list of major events.
Include dates, court info, and parties involved if available.

OUTPUT FORMAT
- Legal Summary: [short paragraph]
- Bullet list of legal events (date, issue, status, parties if known)

What legal issues and litigation history does the company have?
Use trusted public sources, including government and legal databases

OUTPUT FORMAT
Legal Summary: [summarized paragraph]

- Bullet list format:
  - [Date] – [Case Name]: [Details]
""",
tasks=[litigation_history, litigation_review]
)

due_diligence_agent = TeamAgentFactory.create(
    name="Due Diligence Team Agent",
    description="An agent that prepares a sumamry about a company as a due diligence document",
    instructions="""
Combine information from the following:

General company info

Financial records

Legal records

Online sentiment and reviews

Summarize the company's overall status across the above categories in under 300 words.
""",
agents=[knowledge_gathering_agent, litigation_agent]
)

result = due_diligence_agent.run("Datadog", max_iterations=50)
print(result.data.output)
print(json.dumps(result["data"]["intermediate_steps"], indent=4))

knowledge_gathering_agent.deploy()
print("Knowledge Gathering Agent deployed successfully.")
litigation_agent.deploy()
print("Litigation Agent deployed successfully.")
due_diligence_agent.deploy()
print("Due Diligence Team Agent deployed successfully.")

# agent = AgentFactory.get("684acfc79742d9ed28e12447")
# response = agent.run("Datadog", max_iterations=50)
# print(response.data.output)