# 🧾 Receipt Extraction Agent

## Overview

The Receipt Extraction Agent is an AI‑powered assistant that converts image or PDF receipts into a clean, typed JSON record of all key accounting fields. Built with aiXplain’s Agent SDK, it eliminates manual data entry for expense processing, accounting, and analytics workflows.

## Core Features

- 🔍 Automatic OCR & PDF parsing - Picks the right model tool (OCR for images, Docling for PDFs) to extract text from any receipt format.

- 🗃 Field‑level extraction & validation - Returns Pretax Amount, Tax Amount, Total, Supplier Info, VAT Number, List of Goods Purchased, and Cost‑Centre Category.

- 🧑‍💻 Strongly‑typed JSON output - Uses a Pydantic schema so downstream systems always receive predictable keys and data types.

- 🔄 Multi‑task workflow - Separate tasks for scraping images, scraping PDFs, and extracting categories, orchestrated inside one agent.

- ☁️ One‑line deploy - Expose the agent as an HTTP endpoint for dashboards, RPA, or mobile expense apps.

## How It Works

- File ingestion - The user uploads an image or PDF receipt.

- Text extraction - The agent calls aiXplain OCR (646f5ce8…) for images or Docling (677bee6…) for PDFs.

- Category extraction - An LLM maps raw text into the seven target fields.

- Validation - Output is checked against the ReceiptOutput Pydantic model before delivery.

## Installation

```bash
pip install -q aixplain
```

## Setup

```python
import os
os.environ["AIXPLAIN_API_KEY"] = "YOUR_AIXPLAIN_KEY"
os.environ["NUMEXPR_NUM_THREADS"] = "8"  # optional
os.environ["NUMEXPR_MAX_THREADS"] = "8"
```

## Usage

### Create the Agent

```python
from aixplain.factories import AgentFactory
from aixplain.modules.agent.agent_task import AgentTask
from aixplain.modules.agent import OutputFormat

# Define tasks (simplified)
scrape_image = AgentTask(
    name="scrape_image",
    description="Scrapes images to extract information",
    expected_output="Scraped image output."
)

scrape_pdf = AgentTask(
    name="scrape_pdf",
    description="Scrapes PDFs to extract information",
    expected_output="Scraped PDF output."
)

extract_categories = AgentTask(
    name="extract_categories",
    description="Extracts structured categories from the receipt text",
    expected_output="JSON formatted categories."
)

receipt_agent = AgentFactory.create(
    name="Receipt Agent",
    description="Extracts key financial data from receipts.",
    instructions="""
    For the given image or PDF file, use either the OCR tool or the PDF tool to extract text.
    Then use the text to fill the JSON schema with:
    Pretax Amount, Tax Amount, Total, Supplier Info, VAT Number, List of Goods, Cost Centre Category.
    """,
    tasks=[scrape_image, scrape_pdf, extract_categories],
    tools=[
        AgentFactory.create_model_tool(model="646f5ce8cfb5f83af659e392"),  # OCR
        AgentFactory.create_model_tool(model="677bee6c6eb56331f9192a91")   # Docling (PDF)
    ],
)
```

### Define the Output Schema

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: str
    quantity: Optional[int] = 1
    unit_price: Optional[float] = None

class ReceiptOutput(BaseModel):
    pretax_amount: float                = Field(..., alias="Pretax Amount")
    tax_amount: float                   = Field(..., alias="Tax Amount")
    total: float                        = Field(..., alias="Total")
    supplier_info: str                  = Field(..., alias="Supplier Info")
    vat_number: Optional[str]           = Field(None, alias="VAT Number")
    items: List[LineItem]               = Field(..., alias="List of Goods Purchased")
    cost_centre_category: Optional[str] = Field(None, alias="Cost Centre Category")
```

### Run the Agent

```python
receipt_file = "receipt.jpg"  # or a PDF file

response = receipt_agent.run(
    "Extract categories from this receipt:",
    content=[receipt_file],
    output_format=OutputFormat.JSON,
    expected_output=ReceiptOutput
)

print(response.data.output)  # validated JSON string
```

### Deploy

```python
receipt_agent.deploy()
```


## Example Output

```{}
{
  "Pretax Amount": 23.45,
  "Tax Amount": 2.35,
  "Total": 25.80,
  "Supplier Info": "Coffee House, 123 Main St, Boston MA",
  "VAT Number": "US123456789",
  "List of Goods Purchased": [
    { "description": "Latte 12oz", "quantity": 1, "unit_price": 4.00 },
    { "description": "Blueberry Muffin", "quantity": 2, "unit_price": 3.50 }
  ],
  "Cost Centre Category": "Client Meeting Meals"
}
```

## Data Source

📸 All sample receipts in the cookbook are synthetic. Replace them with your own scanned images or PDFs for real‑world testing.