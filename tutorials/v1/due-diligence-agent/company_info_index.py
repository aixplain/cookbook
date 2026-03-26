import os
import csv

os.environ["AIXPLAIN_API_KEY"] = "<YOUR_API_KEY>"  

from aixplain.factories import IndexFactory
from aixplain.modules.model.record import Record


index = IndexFactory.create(
    name="CompanyIndex",
    description="Index for global companies with employee size, domain, and location info"
)

records = []

csv_path = "companies_sorted.csv"  

print("Index id:", index.id)

# Load and convert each row into a Record
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        id = row["name"].lower().replace(" ", "_")
        value = (
            f"Company: {row['name']} | "
            f"Domain: {row['domain']} | "
            f"Founded: {row['year founded']} | "
            f"Industry: {row['industry']} | "
            f"Size: {row['size range']} | "
            f"Location: {row['locality']}, {row['country']} | "
            f"LinkedIn: {row['linkedin url']} | "
            f"Current Employees: {row['current employee estimate']} | "
            f"Total Employees: {row['total employee estimate']}"
        )
        record = Record(id=id, value=value, value_type="text")
        records.append(record)

# Upsert in batches of 500
for i in range(0, len(records), 500):
    index.upsert(records[i: i + 500])
    print(f"✅ Upserted {i + min(500, len(records) - i)} records. Current count: {index.count()}")

# Retrieve the index
index = IndexFactory.get(index.id)


# Sample semantic search
query = "IT companies with large employee base in India"
response = index.search(query)
print(response.details)

