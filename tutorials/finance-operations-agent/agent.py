import os
import csv

os.environ["AIXPLAIN_API_KEY"] = "<YOUR_AIXPLAIN_API_KEY>"
os.environ["NUMEXPR_NUM_THREADS"] = "8"
os.environ["NUMEXPR_MAX_THREADS"] = "8" 

from aixplain.factories import AgentFactory, ModelFactory, IndexFactory
from aixplain.modules.model.record import Record
import json
import logging
import warnings

# Suppress warningsS
warnings.filterwarnings("ignore")

# Suppress logging
logging.getLogger().setLevel(logging.ERROR)

data = [
    {
        "id": "1",
        "pdf_url":"https://huggingface.co/datasets/AyoubChLin/northwind_Shipping_orders/resolve/main/order_10264.pdf",
    },
    {
        "id": "2",
        "pdf_url":"https://huggingface.co/datasets/AyoubChLin/northwind_Shipping_orders/resolve/main/order_10248.pdf",
    },
    {
        "id": "3",
        "pdf_url":"https://huggingface.co/datasets/AyoubChLin/northwind_Shipping_orders/resolve/main/order_10249.pdf",
    },
    {
        "id": "4",
        "pdf_url":"https://huggingface.co/datasets/AyoubChLin/northwind_Shipping_orders/resolve/main/order_10253.pdf",
    }
]

docling = ModelFactory.get("677bee6c6eb56331f9192a91")

index = IndexFactory.create(name="Receipt Index", description="Index for Receipt Documents")
print(index.id)

records = []

for doc in data:
    text = docling.run(doc["pdf_url"]).data
    record = Record(id=doc["id"], value=text, attributes={"source": doc["pdf_url"]})
    records.append(record)

for i in range(0, len(records), 100):
    index.upsert(records[i:i+100])

print("Total documents in index: ", index.count())

finance_ops_agent = AgentFactory.create(
    name="Finance Operations Agent",
    description="An agent that validates financial documents",
    instructions="""
You are a financial operations specialist. You need to ensure that company expenses are legitimate, compliant with policy, and correctly categorized.
Pull relevant details from company receipt index of (PDFs)—vendor name, amount, date, category, etc.
Use the google search tool to fetch contextual information from vendor websites or third-party sources (e.g., verify if a vendor is legitimate.
""",
tools=[
    AgentFactory.create_model_tool(index.id), # Document Index
    AgentFactory.create_model_tool("65c51c556eb563350f6e1bb1") #Google Search SERP
    ]
)

response = finance_ops_agent.run("What is the $440 purchase from VINET for?")
print(response.data.output)

response = finance_ops_agent.run("Is Toms Spezialitaten a verified shipper?")
print(response.data.output)

response = finance_ops_agent.run("What is the unit price for tofu in the documents and give me the market price for it?")
print(response.data.output)
print(json.dumps(response['data'], indent=2))

finance_ops_agent.deploy()