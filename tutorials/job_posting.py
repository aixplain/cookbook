import os

# Set the TEAM_API_KEY
os.environ["TEAM_API_KEY"] = "3865acfa0e554e9a4f4c950c6c0ef1e709e08ce32e55944ef8eb6e1f6e9830f1"

from aixplain.modules.agent.tool.model_tool import ModelTool
from aixplain.factories import AgentFactory
from aixplain.factories import TeamAgentFactory
from aixplain.modules.agent.agent_task import AgentTask
from aixplain.modules.agent import OutputFormat

# Create ModelTool for Google Search
search_tool = ModelTool(model="65c51c556eb563350f6e1bb1")  # Google search tool

# Define format instructions directly
format_instructions = """
# FORMAT INSTRUCTIONS

Your job posting should follow this exact structure:

## 🚀 Job Title: [TITLE]
📍 **Location:** [LOCATION]
🕒 **Employment Type:** [EMPLOYMENT_TYPE]
💼 **Team:** [TEAM]

---

## 📝 About the Role
[COMPANY_INTRODUCTION]
[ROLE_OVERVIEW]

---

## 🔍 What You'll Do
- [RESPONSIBILITY 1]
- [RESPONSIBILITY 2]
- [RESPONSIBILITY 3]
...

---

## ✅ Qualifications

**Required:**
- [REQUIRED QUALIFICATION 1]
- [REQUIRED QUALIFICATION 2]
...

**Preferred:**
- [PREFERRED QUALIFICATION 1]
- [PREFERRED QUALIFICATION 2]
...

---

## 🌟 Why Join Us
- [BENEFIT 1]
- [BENEFIT 2]
...

---

## 📊 Industry Trends
[INDUSTRY_TRENDS_PARAGRAPH]

---

## 📋 How to Apply
[APPLICATION_PROCESS]
"""

# Define tasks for each specialized agent
company_analysis_task = AgentTask(
    name="analyze_company_culture",
    description="Analyze the company culture, values, and work environment based on the job description.",
    expected_output="Detailed analysis of company culture with key values and work environment aspects."
)

role_analysis_task = AgentTask(
    name="analyze_role_requirements",
    description="Extract and analyze the required skills, qualifications, and responsibilities for the role.",
    expected_output="Structured breakdown of role requirements, skills, and qualifications."
)

job_posting_task = AgentTask(
    name="create_job_posting",
    description="Create a comprehensive and engaging job posting based on the company analysis and role requirements.",
    expected_output="A complete job posting with all necessary sections.",
    dependencies=[company_analysis_task, role_analysis_task]
)

industry_analysis_task = AgentTask(
    name="analyze_industry_trends",
    description="Analyze current industry trends related to this role and identify competitive advantages.",
    expected_output="Analysis of industry trends with recommendations for competitive positioning."
)

# Company Culture Analyst Agent
company_analyst = AgentFactory.create(
    name="Company Culture Analyst V3",
    description="Analyzes company culture and values from job descriptions and company information.",
    instructions="""
    You are a Company Culture Analyst specializing in extracting and analyzing company culture, values, and work environment.

    Your tasks:
    1. Carefully read the job description and any company information
    2. Identify explicit and implicit values mentioned in the description
    3. Analyze the company's work culture (collaborative, autonomous, etc.)
    4. Determine the management style and team structure
    5. Summarize the company benefits and what they reveal about company priorities
    6. Use the Google search tool to research recent company news, culture initiatives, or employee reviews
    7. Incorporate real-world company culture insights to enhance your analysis

    Provide a detailed analysis that a job posting writer can use to create an authentic representation.
    """,
    tasks=[company_analysis_task],
    tools=[search_tool],
    llm_id="67e2f3f243d4fa5705dfa71e"  # DeepSeek V3 03-24
)

# Role Requirements Analyst Agent
role_analyst = AgentFactory.create(
    name="Role Requirements Analyst V3",
    description="Analyzes job requirements, qualifications, and responsibilities in detail.",
    instructions="""
    You are a Role Requirements Analyst specializing in extracting and structuring job requirements.

    Your tasks:
    1. Carefully read the job description
    2. Extract all required technical skills and qualifications
    3. Extract all required soft skills
    4. Identify the core responsibilities and expected deliverables
    5. Categorize requirements as "must-have" vs "nice-to-have"
    6. Determine the seniority level and expected experience
    7. Use the Google search tool to research current industry standards for this role
    8. Find the most in-demand skills and certifications for this position type

    Provide a structured analysis that clearly separates technical requirements, soft skills, responsibilities, and experience levels.
    """,
    tasks=[role_analysis_task],
    tools=[search_tool],
    llm_id="67e2f3f243d4fa5705dfa71e"  # DeepSeek V3 03-24
)

# Job Posting Creator Agent
job_posting_creator = AgentFactory.create(
    name="Job Posting Creator V3",
    description="Creates comprehensive and engaging job postings based on company culture and role requirements.",
    instructions="""
    You are a Job Posting Creator specializing in writing compelling job descriptions.

    Your tasks:
    1. Use the company culture analysis to create an engaging company introduction
    2. Use the role requirements analysis to create detailed, well-structured sections for:
       - Responsibilities
       - Required Qualifications
       - Preferred Qualifications
    3. Add compelling sections about:
       - Growth opportunities
       - Company benefits
       - Application process
    4. Ensure the tone matches the company culture
    5. Use bullet points for readability and highlight key information
    6. Use the Google search tool to research effective job posting strategies
    7. Find examples of successful job postings in the same industry to inform your writing

    Create a complete, professional job posting that would attract qualified candidates.
    """,
    tasks=[job_posting_task],
    tools=[search_tool],
    llm_id="67e2f3f243d4fa5705dfa71e"  # DeepSeek V3 03-24
)

# Industry Analyst Agent
industry_analyst = AgentFactory.create(
    name="Industry Analyst V3",
    description="Analyzes industry trends and competitive landscape for specific roles.",
    instructions="""
    You are an Industry Analyst specializing in job market and industry trends.

    Your tasks:
    1. Analyze the job description to identify the industry and specialized field
    2. Identify current trends in this specific job category
    3. Determine what competitive companies are offering for similar roles
    4. Suggest competitive advantages or unique selling points to highlight
    5. Recommend skill emphasis based on industry demand
    6. Use the Google search tool to research current industry news and trends
    7. Find salary ranges, market demand, and future outlook for this position type

    Provide analysis that helps position this job posting competitively in the current market.
    """,
    tasks=[industry_analysis_task],
    tools=[search_tool],
    llm_id="67e2f3f243d4fa5705dfa71e"  # DeepSeek V3 03-24
)

#Run all the specialized agents
industry_analyst.run("What can you tell me about retail industry?")
job_posting_creator.run("Create a job posting for a technical product manager")
role_analyst.run("Analyze the job posting for a technical product manager")
company_analyst.run("Analyze the company culture for a technical product manager")

# Deploy all the specialized agents
company_analyst.deploy()
role_analyst.deploy()
job_posting_creator.deploy()
industry_analyst.deploy()

# Create the team agent
team = TeamAgentFactory.create(
    name="Job Posting Analysis Team V5",
    description="A team of agents that analyzes company culture and job requirements to create comprehensive job postings.",
    agents=[company_analyst, role_analyst, job_posting_creator, industry_analyst],
    use_mentalist=True,  # Enable dynamic planning
    use_inspector=True,  # Enable output inspection
    #inspector_targets=["steps", "output"],  # Inspect both steps and final output
    llm_id="67e2f3f243d4fa5705dfa71e"  # DeepSeek V3 03-24 for team agent's micro agents
)

# Run the team agent with query and format instructions
print("Running the team agent with query...")
result = team.run(
    query="Create a job posting for an AI Vibe Coder position. This person specializes in creating software through natural language prompts to AI systems, rather than traditional manual coding. They work in the emerging field of 'vibe coding' where developers describe what they want in conversational language and AI models generate the code.",
    content=format_instructions,
    output_format=OutputFormat.MARKDOWN
)
print(result.data["output"])
session_id = result.data["session_id"]

team.run(query="Create a job posting for a technical product manager",
    content=format_instructions,
    output_format=OutputFormat.MARKDOWN)