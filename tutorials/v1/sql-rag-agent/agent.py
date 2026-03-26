import os
os.environ["AIXPLAIN_API_KEY"] = "<YOUR_API_KEY>"

import warnings
import logging
from aixplain.factories import AgentFactory
from aixplain.modules.agent.tool.sql_tool import SQLTool
from aixplain.modules.agent.tool.python_interpreter_tool import PythonInterpreterTool



# Suppress warnings + logs
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)

# SQL tool (SQLite DB must exist already)
sql_tool = SQLTool(
    name="Insurance Database",
    description="SQL access to insurance dataset",
    database="/Users/asmafurniturewala/Desktop/aixplain/SQLRAGAgent/insurance.db",
    enable_commit=False,
    tables=["insurance"]
)

agent = AgentFactory.create(
    name="Insurance Data Analyst",
    description="Agent that answers questions using SQL queries and generates plots with Python.",
    instructions="""You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the below tools. Only use the information returned by the below tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    To start you should ALWAYS look at the tables in the database to see what you can query.
    Do NOT skip this step.
    Then you should query the schema of the most relevant tables.""",
   
    tools=[sql_tool],
    output_format="markdown"
)

