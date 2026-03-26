import os
from datetime import datetime, timedelta

# Set the TEAM_API_KEY
os.environ["TEAM_API_KEY"] = "YOUR-TEAM-API-KEY"

from aixplain.factories import AgentFactory, ModelFactory
from aixplain.factories import TeamAgentFactory
from aixplain.modules.agent.agent_task import AgentTask
from aixplain.modules.agent import OutputFormat

def get_support_data(dummy: str = "unused"):
    """Simulates fetching customer support data.
    This is a placeholder that returns mock customer support metrics.
    In a real application, this would fetch actual data from your system.
    
    Args:
        dummy: Required parameter for AIXplain SDK (not used)
    """
    return """
CUSTOMER SUPPORT METRICS

Ticket Summary:
- Total Tickets: 241
- Login Issues: 50 tickets (21%)
- Billing Issues: 30 tickets (12%)
- Feature Requests: 20 tickets (8%)

Performance Metrics:
- SLA Compliance: 78% (Target: 95%)
- First Response Time: 6.2 hours
- Customer Satisfaction: 3.2/5.0

Channel Distribution:
- Email: 45%
- Live Chat: 30%
- Phone: 20%
- Self-Service: 5%

Key Trends:
- Login issues increasing (15% MoM)
- Support escalations up 40%
- Customer satisfaction declining
"""

# Create and deploy the utility model
print("Setting up support data utility...")

support_data_utility = ModelFactory.create_utility_model(
    name="Support Data Utility v1",
    description="Simulates fetching customer support metrics",
    code=get_support_data
)
print(support_data_utility.__dict__)
support_data_utility.deploy()
# print(f"Utility deployed with ID: {support_data_utility.id}")

# Create the tool that agents will use
support_data_tool = AgentFactory.create_model_tool(
    model=support_data_utility.id,
    description="Tool that returns simulated customer support metrics including ticket volumes, performance metrics, and trends."
)

# Define tasks with clear dependencies
analysis_task = AgentTask(
    name="analyze_support_data",
    description="""Analyze the support metrics:
    1. Call the support data tool to get metrics
    2. Create a clear analysis with these sections:
       - Top Issues (by volume)
       - Performance Metrics
       - Key Trends
    3. Format your response in markdown""",
    expected_output="Markdown formatted analysis of support metrics"
)

optimization_task = AgentTask(
    name="identify_process_bottlenecks",
    description="""Based on the analysis from the Data Analyst:
    1. Review the metrics and trends
    2. List specific process issues found
    3. Recommend improvements for each issue
    4. Format your response in markdown""",
    expected_output="Markdown formatted list of issues and recommendations",
    dependencies=["analyze_support_data"]  # Explicitly depend on analysis task
)

report_task = AgentTask(
    name="compile_coo_report",
    description="""Using both the analysis and optimization results:
    1. Combine the key findings and recommendations
    2. Create an executive summary
    3. Format as a clear markdown report""",
    expected_output="Markdown formatted executive summary",
    dependencies=["analyze_support_data", "identify_process_bottlenecks"]  # Depend on both previous tasks
)

# Configure agents with more explicit instructions
data_analyst = AgentFactory.create(
    name="Data Analyst V6",
    description="Analyzes support metrics",
    instructions="""You are a data analyst. Your task is simple:
    1. Call the support data tool (the parameter value doesn't matter)
    2. Format your analysis in markdown with these sections:
       # Support Metrics Analysis
       ## Top Issues
       - List top issues by volume
       ## Performance Metrics
       - List key metrics and targets
       ## Key Trends
       - List important trends""",
    tasks=[analysis_task],
    tools=[support_data_tool],
    llm_id="67fd9d6aef0365783d06e2ee"  # GPT-4.1
)

process_optimizer = AgentFactory.create(
    name="Process Optimizer V6",
    description="Recommends support process improvements",
    instructions="""You are a process optimizer. Your task is simple:
    1. Review the analysis from the Data Analyst
    2. Format your response in markdown:
       # Process Analysis
       ## Issues Identified
       - List each issue
       ## Recommendations
       - For each issue, provide a specific recommendation""",
    tasks=[optimization_task],
    llm_id="67fd9d6aef0365783d06e2ee"  # GPT-4.1
)

report_writer = AgentFactory.create(
    name="Report Writer V6",
    description="Creates executive summaries",
    instructions="""You are a report writer. Your task is simple:
    1. Review both the analysis and recommendations
    2. Create a markdown report:
       # Executive Summary
       ## Key Findings
       - List most important metrics and trends
       ## Recommendations
       - List key recommendations""",
    tasks=[report_task],
    llm_id="67fd9d6aef0365783d06e2ee"  # GPT-4.1
)

# Deploy agents
print("\nDeploying agents...")
data_analyst.deploy()
process_optimizer.deploy()
report_writer.deploy()

# Create team with explicit task ordering
print("Creating analysis team...")
support_team = TeamAgentFactory.create(
    name="Support Analysis Team V6",
    description="Analyzes support metrics and recommends improvements",
    agents=[data_analyst, process_optimizer, report_writer],
    use_mentalist=True,  # For task planning
    use_inspector=True,  # For error handling
    llm_id="67fd9d6aef0365783d06e2ee"  # GPT-4.1
)

# Run analysis with increased timeout and iterations
print("\nRunning analysis...")
try:
    result = support_team.run(
        query="""Please complete these tasks in order:
        1. Analyze the support metrics
        2. Identify issues and recommend improvements
        3. Create an executive summary""",
        output_format=OutputFormat.MARKDOWN,
        max_iterations=30,  # Increased from 50
        timeout=600  # 10 minute timeout
    )
    
    print("\n=== Analysis Results ===")
    print("="*80)
    print(result.data["output"])
    
    print("\n=== Debug: Execution Steps ===")
    print("="*80)
    from pprint import pprint
    pprint(result.data["intermediate_steps"])

except Exception as e:
    print(f"\nError during execution: {str(e)}")
    print("\nDebug: Execution trace:")
    try:
        pprint(result.data["intermediate_steps"])
    except:
        print("No execution trace available")
