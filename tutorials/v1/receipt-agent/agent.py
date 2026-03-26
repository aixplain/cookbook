import os

os.environ["AIXPLAIN_API_KEY"] = "YOUR_AIXPLAIN_KEY"
os.environ["NUMEXPR_NUM_THREADS"] = "8"  # optional
os.environ["NUMEXPR_MAX_THREADS"] = "8"

from aixplain.factories import AgentFactory, TeamAgentFactory
from aixplain.modules.agent.agent_task import AgentTask
from aixplain.modules.agent import OutputFormat
import json
import logging
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Suppress logging
logging.getLogger().setLevel(logging.ERROR)

from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: str                    
    quantity: Optional[int] = 1
    unit_price: Optional[float] = None  # price per item, if available

class ReceiptOutput(BaseModel):
    pretax_amount: float                = Field(..., alias="Pretax Amount")
    tax_amount:   float                 = Field(..., alias="Tax Amount")
    total:        float                 = Field(..., alias="Total")
    supplier_info: str                  = Field(..., alias="Supplier Info")
    vat_number:   Optional[str] = Field(None, alias="VAT Number")
    items:        List[LineItem]        = Field(..., alias="List of Goods Purchased")
    cost_centre_category: Optional[str] = Field(
        None, alias="Cost Centre Category"
    )

scrape_image = AgentTask(
    name="scrape_image",
    description="Scrapes images to extract information",
    expected_output="Scraped image output."
)

scrape_pdf=AgentTask(
    name="scrape_pdf",
    description="Scrapes pdfs to extract information", 
    expected_output="Scraped pdf output"
)

extract_categories = AgentTask(
    name="extract_categories",
    description="From the scraped information, extract the necessary categories",
    expected_output="JSON formatted categories."
)

receipt_agent = AgentFactory.create(
    name="Receipt Agent",
    description="An agent that extracts information from image and pdf receipts and extracts relevant information",
    instructions="""
    For the given image or pdf file, use either the OCR tool or the PDF tool, to extract text from the file. 
    Then use the text to extract categories and display the JSON output to the user. 

    The categories for the output are:
    1) Pretax Amount, 
    2) Tax Amount, 
    3) Total, 
    4) Supplier Info, 
    5) VAT Number,
    6) List of Goods purchased, 
    7) Cost Centre Category
""",
tasks=[scrape_image, scrape_pdf, extract_categories],
tools=[
    AgentFactory.create_model_tool(model="646f5ce8cfb5f83af659e392"), #OCR
    AgentFactory.create_model_tool(model="677bee6c6eb56331f9192a91") #docling
],
)

receipt_file="receipt_exmaple.jpg"

result = receipt_agent.run("Extract categories from this file and respond in JSON format: ", content=[receipt_file], output_format=OutputFormat.JSON, expected_output=ReceiptOutput )
print(result.data.output)
print(json.dumps(result["data"], indent=2))

receipt_agent.deploy()