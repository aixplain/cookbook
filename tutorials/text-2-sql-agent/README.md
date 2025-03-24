# Text2SQL Agent

This project implements a Text2SQL agent designed to generate and evaluate SQLite queries based on user-provided natural language questions. The agent uses the aiXplain framework to parse prompts, generate SQL queries following a strict schema, and validate the results against ground truths.

## Features

* **Automated SQL Generation:** Converts natural language questions into syntactically correct SQLite queries.
* **Schema Adherence:** Enforces strict adherence to the provided database schema (California schools).
* **Validation and Evaluation:** Executes the generated SQL queries against a SQLite database and compares results with ground truth queries.
* **Integrated Tools:** Utilizes a Python interpreter and SQL execution tool from the aiXplain framework.

## Requirements

* Python 3.6+
* SQLite3
* [aiXplain](https://github.com/aixplain/aiXplain) (installed from GitHub)
* Standard Python libraries: `os`, `re`, `json`, `sqlite3`

## Setup

1. **Clone the Repository**

   Clone or download the repository containing the Text2SQL agent code.
2. **Install Dependencies**

   Install the required package by running:

   <pre class="!overflow-visible" data-start="1155" data-end="1241"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none rounded-t-[5px]">bash</div><div class="sticky top-9"><div class="absolute bottom-0 right-0 flex h-9 items-center pr-2"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none px-4 py-1" aria-label="Copy"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-xs"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>Copy</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre language-bash"><span><span>pip install aixplain --upgrade</span></span></code></div></div></pre>
3. **Prepare the Database**

   * Ensure you have the `california_schools.sqlite` file in your working directory.
   * The code automatically converts the SQLite file to a `.db` file for querying.
4. **Configuration**

   * Set the `TEAM_API_KEY` environment variable if needed.
   * Confirm the schema file (`california_schools.schema`) and ground truth file (`dev.json`) are in the correct locations.

## Code Structure

* **Imports and Environment Setup:**

  Installs the aiXplain package and sets up the environment variable for the API key.
* **Prompt Definitions:**

  Contains detailed SQL agent prompts and guidelines to ensure the generated SQL queries are correct, efficient, and schema-compliant.
* **Utility Functions:**

  * `read_data(file)`: Reads text data from a file.
  * `read_binary(file)`: Reads a binary file (e.g., SQLite database), converts file extensions, and writes the new file.
  * `read_json(file)`: Reads JSON data from a file.
* **Schema and Ground Truth Loading:**

  Loads the California schools schema and ground truth queries from respective files.
* **Agent Initialization:**

  Creates the Text2SQL agent using the aiXplain framework, providing it with the SQL prompt, Python interpreter, and SQL execution tool.
* **Query Generation and Execution:**

  Iterates over a set of natural language queries:

  * Generates the corresponding SQL query using the agent.
  * Evaluates the query by executing it against the SQLite database.
  * Compares the results with ground truth answers and calculates the final accuracy.
* **Result Evaluation:**

  The evaluation function `execute_sql` compares the generated SQL output with the ground truth result set, reporting an overall accuracy percentage.

## Usage

1. **Run the Notebook or Script:**

   Execute the Jupyter Notebook or Python script. The agent will generate SQL queries for each input question, execute them, and print the final accuracy.
2. **Review the Output:**

   The final accuracy of the SQL queries is printed to the console, providing a measure of the agent’s performance.

## Notes

* The agent is designed to handle SQL generation within the constraints of SQLite and the specific database schema provided.
* All column names that include spaces are automatically enclosed in backticks to ensure SQL syntax correctness.
* The project emphasizes the importance of adhering to the provided schema, ensuring that no unsupported SQL functions or clauses are used.

## Acknowledgments

* Developed using the aiXplain framework.
* Inspired by the challenges of automating SQL query generation from natural language inputs.

Enjoy using the Text2SQL Agent!
