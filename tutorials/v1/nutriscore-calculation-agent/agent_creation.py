from nutriscore.nutriscore import get_nutriscore
from nutriscore.nutriscore_beverage import get_nutriscore_beverage_score
from nutriscore.nutriscore_cooking_fats import get_nutriscore_cooking_fat_score
from aixplain.factories import AgentFactory


from aixplain.enums import DataType
from aixplain.factories import ModelFactory
from aixplain.modules.model.utility_model import UtilityModelInput


try:
    nutriscore_default_utility = ModelFactory.get(model_id="67bede734547417162861ac6")
except Exception:
    print("creating tool")
    nutriscore_default_utility = ModelFactory.create_utility_model(
        name="Nutriscore 1",
        description="Nutriscore default score calculation function",
        code=get_nutriscore,
        inputs=[
            UtilityModelInput(
                name="energy_kcal",
                description="Energy content in kcal.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="sugars_g",
                description="Sugar content in grams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="sat_fat_g",
                description="Saturated fat content in grams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="salt_mg",
                description="Salt content in milligrams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="fruit_veg_percent",
                description="Percentage of fruit and vegetables.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="fibre_g",
                description="Fiber content in grams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="protein_g",
                description="Protein content in grams.",
                type=DataType.NUMBER,
            ),
        ],
    )
    print(f"nutriscore_default_utility={nutriscore_default_utility.id}")

try:
    nutriscore_beverage_utility = ModelFactory.get(model_id="67bede75058286b62912e280")
except Exception:
    print("creating tool")
    nutriscore_beverage_utility = ModelFactory.create_utility_model(
        name="Nutriscore Beverage 4",
        description="Nutriscore score calculation function for beverages",
        code=get_nutriscore_beverage_score,
        inputs=[
            UtilityModelInput(
                name="energy_kcal",
                description="Energy content in kcal.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="sugars_g",
                description="Sugar content in grams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="sat_fat_g",
                description="Saturated fat content in grams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="salt_mg",
                description="Salt content in milligrams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="fruit_veg_percent",
                description="Percentage of fruit and vegetables.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="fibre_g",
                description="Fiber content in grams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="protein_g",
                description="Protein content in grams.",
                type=DataType.NUMBER,
            ),
        ],
    )
    print(f"nutriscore_beverage_utility={nutriscore_beverage_utility.id}")

try:
    nutriscore_cooking_fat_utility = ModelFactory.get(
        model_id="67bede77058286b62912e281"
    )
except Exception:
    print("creating tool")
    nutriscore_cooking_fat_utility = ModelFactory.create_utility_model(
        name="Nutriscore Fats 5",
        description="Nutriscore score calculation function for cooking fats",
        code=get_nutriscore_cooking_fat_score,
        inputs=[
            UtilityModelInput(
                name="sat_fat_g",
                description="Saturated fat content in grams.",
                type=DataType.NUMBER,
            ),
            UtilityModelInput(
                name="total_fat_g",
                description="Total fat content in grams.",
                type=DataType.NUMBER,
            ),
        ],
    )
    print(f"nutriscore_cooking_fat_utility={nutriscore_cooking_fat_utility.id}")

# try:
#     nutriscore_classification_utility = ModelFactory.get(
#         model_id="67bed5ed058286b62912e25e"
#     )
# except Exception:
#     print("creating tool")
#     nutriscore_classification_utility = ModelFactory.create_utility_model(
#         name="Nutriscore Class 3",
#         description="Nutriscore Classification function used to categorize nutriscore real value into Nutriscore category",
#         code=nutriscore_classification,
#         inputs=[
#             UtilityModelInput(
#                 name="score",
#                 description="Real number representing nutriscore from -15 to +40",
#                 type=DataType.NUMBER,
#             ),
#         ],
#     )
#     print(f"nutriscore_classification_utility={nutriscore_classification_utility.id}")

ROLE = """
You are a chatbot designed to calculate the Nutri-Score of food based on its nutritional content.
The Nutri-Score is a 5-Colour Nutrition label rating system.

When a user requests a Nutri-Score calculation, follow these steps:

    1. Classify the food into one of three categories:
        a. Beverages
        b. Cooking fats
        c. Other (default)
        Always ask the user to specify the category unless already provided.
    2. Collect all required macronutrients for classified food category. If an image is provided use OCR to extract macronutrients automatically, prompting the user for any missing ones.
    3. Call the appropriate Nutri-Score tool based on the food category to get nutriscore score. You must always calculate this by calling a tool.

If any information is missing, ask the user for clarification before proceeding. If an answer cannot be provided, inform the user accordingly.

When providing nutriscore output it in this format: Nutri-Score of provided food is <nutriscore>.
"""
agent = AgentFactory.create(
    name="NutriScore agent",
    instructions=ROLE,
    description="Agent that calculates NutriScore value of given food. Can use OCR to extract macronutriens from image.",
    tools=[
        AgentFactory.create_model_tool(
            model=nutriscore_default_utility.id,
            description="Tool to calculate nutriscore given macros as input",
        ),
        AgentFactory.create_model_tool(
            model=nutriscore_cooking_fat_utility.id,
            description="Tool to calculate nutriscore for cooking fats given macros as input",
        ),
        AgentFactory.create_model_tool(
            model=nutriscore_beverage_utility.id,
            description="Tool to calculate nutriscore for beverages given macros as input",
        ),
        # AgentFactory.create_model_tool(model=nutriscore_classification_utility.id, description='Tool to categorize nutriscore real value into Nutriscore category(A/B/C/D/E)'),
        AgentFactory.create_model_tool(
            model="646f5ce8cfb5f83af659e392",
            description="OCR tool to get product macronutrients from image.",
        ),
    ],
)
print(f"{agent.id=}")
