import os
import shutil
import json
import re
import random
import sqlite3
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from collections import defaultdict
from typing import List, Dict, Text
from aixplain.modules.model.record import Record 
from aixplain.factories import ModelFactory, AgentFactory, TeamAgentFactory

def __parse_question_chunks(text: Text, chunk_size: int = 1000) -> List[Text]:
    """Chunk natural language questions using sentence-aware splitting"""
    if not text.strip():
        return []

    chunks = []
    current_chunk = []
    current_length = 0
    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:
        sentence_length = len(sentence)
        
        # Split long sentences into sub-chunks
        if sentence_length > chunk_size:
            sub_chunks = [sentence[i:i+chunk_size] for i in range(0, sentence_length, chunk_size)]
            for sub in sub_chunks:
                if current_length + len(sub) > chunk_size:
                    if current_chunk:
                        chunks.append(" ".join(current_chunk))
                    current_chunk = [sub]
                    current_length = len(sub)
                else:
                    current_chunk.append(sub)
                    current_length += len(sub) + 1
        else:
            if current_length + len(sentence) + 1 > chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = len(sentence)
            else:
                current_chunk.append(sentence)
                current_length += len(sentence) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def __parse_sql_chunks(sql: Text, chunk_size: int = 1000) -> List[Text]:
    """Chunk SQL queries while preserving syntax structure"""
    if not sql.strip():
        return []

    chunks = []
    current_chunk = []
    current_length = 0
    tokens = sql.split()
    
    for token in tokens:
        token_length = len(token) + 1  # Account for space
        
        if current_length + token_length > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
            
            # Handle over-sized tokens
            while len(token) > chunk_size:
                chunks.append(token[:chunk_size])
                token = token[chunk_size:]
                current_length = len(token)
            
            if token:
                current_chunk.append(token)
                current_length += len(token) + 1
        else:
            current_chunk.append(token)
            current_length += token_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def process_train_data(file_path: str, chunk_size: int = 1000) -> List[Record]:
    """Process training data with proper chunking for different field types"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    records = []
    
    for entry in data:
        db_id = entry.get("db_id", "").strip()
        evidence = entry.get("evidence", "").strip()
        question = entry.get("question", "").strip()
        sql_query = entry.get("SQL", "").strip()

        docs = f"""Question: {question}; \nSQL: {sql_query}"""

        # Process questions with sentence-aware chunking
        question_chunks = __parse_question_chunks(docs, chunk_size)
        for chunk in question_chunks:
            records.append(
                            Record(
                                value=chunk,
                                attributes={
                                    "Database Id": db_id,
                                    "Evidence": evidence,
                                }
                                ))

        # # Process SQL with syntax-aware chunking
        # sql_chunks = __parse_sql_chunks(sql_query, chunk_size)
        # for chunk in sql_chunks:
        #     records.append(
        #         Record(
        #             value=chunk,
        #             attributes={
        #                 "db_id": db_id,
        #                 "type": "sql_query",
        #                 "full_query": sql_query
        #                 "evidence": evidence,
        #             }
        #     ))

    return records

def rename_and_save_sqlite(original_path, base_dir="dev_databases"):
    """
    Rename a .sqlite file to .db and save it under dev_databases/<db_id>/<db_id>.db
    Skip if the .db version already exists.

    Args:
        original_path (str): Path to the original .sqlite file.
        base_dir (str): Root directory to save the .db files.

    Returns:
        str: Final path of the .db file.
    """
    if not os.path.isfile(original_path):
        raise FileNotFoundError(f"File not found: {original_path}")

    # Infer db_id from parent directory name
    db_id = os.path.basename(os.path.dirname(original_path))

    # Target .db path
    target_dir = os.path.join(base_dir, db_id)
    os.makedirs(target_dir, exist_ok=True)

    target_path = os.path.join(target_dir, f"{db_id}.db")

    # Skip if .db already exists
    if os.path.exists(target_path):
        print(f"[✓] Target .db already exists: {target_path}")
        return target_path

    # Otherwise, rename and save
    shutil.copyfile(original_path, target_path)
    print(f"[+] Renamed and saved as: {target_path}")
    return target_path


def retrieve_docs(query, model_id, num_results):
    """
    Retrieves documents from a model based on the query.
    :param query: The query string to search for.
    :param model_id: The ID of the model to use for retrieval.
    :param num_results: The number of results to retrieve.
    :return: A string containing the retrieved documents.
    """
    try:
        index_model = ModelFactory.get(model_id)  # Retrieves the model by ID
        response = index_model.run(query, parameters={"numResults": num_results})
        details = response.get("details", [])
        limited_details = details[:num_results]
        retrieved = "\n\n".join([r["data"] for r in limited_details if r and r.get("data")])
        return retrieved
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def decouple_question_schema(dataset_dir, dataset_name):
    """
    Decouples the question and schema from the dataset.
    :param dataset_dir: Directory containing the dataset.
    :param dataset_name: Name of the dataset.
    :return: Tuple containing question list, database path list, knowledge list, and output data.
    """
    dataset_path = os.path.join(dataset_dir, dataset_name, "dev.json")
    db = "dev_databases" if dataset_name == "bird" else "database"
    db_root_path = os.path.join(dataset_dir, dataset_name, db)

    with open(dataset_path, "r", encoding="utf8") as file:
        datasets = json.load(file)

    question_list = []
    db_path_list = []
    knowledge_list = []
    output_data = {
        "question_id": [],
        "difficulty": [],
        "field": [],
        "sql_path": [],
        "schema": [],
        "question": [],
        "prediction": [],
        "ground_truth": [],
    }

    for i, data in enumerate(datasets):
        basename = f"{data.get('db_id', '')}.sqlite"
        path = os.path.join(db_root_path, data.get("db_id", ""), basename)
        db_path_list.append(path)
        schema_path = os.path.join(dataset_name, f"{data['db_id']}.txt")
        schema = open(schema_path, "r", encoding="utf8").read()
        question_list.append(data.get("question", ""))
        knowledge_list.append(data.get("evidence", None))

        output_data["question_id"].append(data.get("question_id", None) or i)
        output_data["difficulty"].append(data.get("difficulty", None))
        output_data["field"].append(data.get("db_id", None))
        output_data["question"].append(data.get("question", None))
        output_data["ground_truth"].append(data.get("SQL", "") or data.get("query", ""))
        output_data["sql_path"].append(path)
        output_data["schema"].append(schema)

    return question_list, db_path_list, knowledge_list, output_data


def select_fixed_total_samples(output, total_samples=100):
    """
    Select a fixed number of samples from the output data, ensuring a balanced selection across different databases.
    :param output: The output data containing question IDs and other information.
    :param total_samples: The total number of samples to select.
    :return: A list of selected entries.
    """
    db_to_entries = defaultdict(list)

    for i, db_id in enumerate(output["field"]):
        entry = {
            "question_id": output["question_id"][i],
            "difficulty": output["difficulty"][i],
            "db_id": db_id,
            "question": output["question"][i],
            "prediction": output["prediction"][i] if output["prediction"] else None,
            "ground_truth": output["ground_truth"][i],
            "sql_path": output["sql_path"][i],
            "schema": output["schema"][i],
        }
        db_to_entries[db_id].append(entry)

    num_dbs = len(db_to_entries)
    base_per_db = total_samples // num_dbs

    selected_entries = []
    for db, entries in db_to_entries.items():
        if len(entries) >= base_per_db:
            selected = random.sample(entries, base_per_db)  # Pick random
        else:
            selected = entries

        selected_entries.extend(selected)

    remaining_slots = total_samples - len(selected_entries)
    if remaining_slots > 0:
        all_entries = [(db, entry) for db, entries in db_to_entries.items() for entry in entries if len(entries) > base_per_db]
        selected_extra = random.sample(all_entries, remaining_slots)

        selected_entries.extend([entry for _, entry in selected_extra])

    if len(selected_entries) > total_samples:
        selected_entries = random.sample(selected_entries, total_samples)

    return selected_entries


def process_and_save_results(responses, output, output_dir, start=0):
    """
    Process the responses and save them to JSON files.
    :param responses: List of responses from the model.
    :param output: The output data containing question IDs and other information.
    :param output_dir: Directory to save the results.
    :param start: Starting index for processing.
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, (response, data) in enumerate(zip(responses, output[start:]), start=start):
        output_data = {
            "question_id": data["question_id"],
            "difficulty": data["difficulty"] if data["difficulty"] is not None else "Undefined",
            "field": data["db_id"],
            "sql_path": data["sql_path"],
            "question": data["question"],
            "prediction": response,
            "ground_truth": data["ground_truth"],
        }

        print(f"{i}. {data['question']}")
        print("   ", response.replace("\t", " ").replace("\n", " "))
        print()

        result_file_path = os.path.join(output_dir, f"result_{i}.json")
        with open(result_file_path, "w", encoding="utf-8") as file:
            json.dump(output_data, file, indent=4, ensure_ascii=False)
    print(f"Results successfully saved in {output_dir}")


def execute_sql(predicted_sql, ground_truth, db_path):
    """
    Execute the SQL queries and compare the results.
    :param predicted_sql: The SQL query generated by the model.
    :param ground_truth: The ground truth SQL query.
    :param db_path: The path to the SQLite database.
    :return: 1 if the results match, 0 otherwise.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(predicted_sql)
        predicted_res = cursor.fetchall()

        cursor.execute(ground_truth)
        ground_truth_res = cursor.fetchall()

        conn.close()

        return 1 if set(predicted_res) == set(ground_truth_res) else 0
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return 0


def sql_res(predicted_sql, ground_truth, db_path):
    """
    Execute the SQL queries and return the results.
    :param predicted_sql: The SQL query generated by the model.
    :param ground_truth: The ground truth SQL query.
    :param db_path: The path to the SQLite database.
    :return: The results of the SQL queries.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(predicted_sql)
        predicted_res = cursor.fetchall()

        cursor.execute(ground_truth)
        ground_truth_res = cursor.fetchall()

        conn.close()

        return predicted_res, ground_truth_res
    except Exception as e:
        return f"Error: {e}"


def evaluate_predictions(output_dir, start=0, end=None):
    """
    Evaluate SQL predictions by executing them against the database and comparing results.
    :param output_dir: Directory containing the output files.
    :param start: Starting index for processing files.
    :param end: Ending index for processing files.
    :return: Accuracy by difficulty level and final accuracy.
    """
    replacements = {r"\n": " ", r"```": "", r";": "", r":": "", r"(?i)sql": ""}
    # Initialize counters for difficulty-based evaluation
    difficulty_count = defaultdict(int)
    difficulty_correct = defaultdict(int)

    # Initialize counters for overall SQL prediction evaluation
    total_correct, num_files = 0, 0

    files = sorted(f for f in os.listdir(output_dir) if f != "results")
    files = files[start:end] if end else files[start:]  # Limit files based on start:end range

    for i, path in enumerate(files):
        file_path = os.path.join(output_dir, path)
        if path == "results" or not os.path.isfile(file_path):
            continue

        num_files += 1

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                out_data = json.load(f)

            required_keys = {"prediction", "ground_truth", "sql_path"}
            if set(required_keys).issubset(out_data):
                for pattern, replacement in replacements.items():
                    out_data["prediction"] = re.sub(pattern, replacement, out_data["prediction"])

                res = execute_sql(out_data["prediction"], out_data["ground_truth"], out_data["sql_path"])

                if "difficulty" in out_data:
                    difficulty = out_data["difficulty"]
                    difficulty_count[difficulty] += 1
                    if res == 1:
                        difficulty_correct[difficulty] += 1

                total_correct += res
                if res == 0:
                    print(f"Incorrect Prediction {i}: {out_data['prediction']}")

            else:
                print(f"Skipping {file_path}: Missing required keys.")

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Calculate and print accuracy for each difficulty level
    accuracy_by_difficulty = {}
    for difficulty, count in difficulty_count.items():
        if count > 0:
            accuracy = (difficulty_correct[difficulty] / count) * 100
            accuracy_by_difficulty[difficulty] = f"{accuracy:.2f}% of {count}"
        else:
            accuracy_by_difficulty[difficulty] = "No valid files found"

    # Compute final accuracy for all SQL predictions
    final_accuracy = f"{(total_correct / num_files * 100):.2f}%" if num_files > 0 else "No valid files found"

    print("Accuracy by Difficulty:", accuracy_by_difficulty)
    print("Final SQL Prediction Accuracy:", final_accuracy)

    return accuracy_by_difficulty, final_accuracy


def evaluate_sql_predictions(output_dir, start=0, end=None):
    """
    Evaluate SQL predictions by executing them against the database and comparing results.
    :param output_dir: Directory containing the output files.
    :param start: Starting index for processing files.
    :param end: Ending index for processing files.
    :return: Final accuracy of SQL predictions.
    """
    replacements = {r"\n": " ", r"```": "", r";": "", r":": "", r"(?i)sql": ""}
    total_correct, num_files = 0, 0
    files = sorted(f for f in os.listdir(output_dir) if f != "results")

    # Limit files based on start:end range
    files = files[start:end] if end else files[start:]

    for i, path in enumerate(files):
        file_path = os.path.join(output_dir, path)
        if path == "results" or not os.path.isfile(file_path):
            continue

        num_files += 1

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                out_data = json.load(f)

            required_keys = {"prediction", "ground_truth", "sql_path"}
            if required_keys.issubset(out_data):
                # Clean prediction: Remove markdown code fences, 'sql' substring, and newlines
                for pattern, replacement in replacements.items():
                    out_data["prediction"] = re.sub(pattern, replacement, out_data["prediction"])

                # Execute SQL and compute results
                res = execute_sql(out_data["prediction"], out_data["ground_truth"], out_data["sql_path"])
                p, g = sql_res(out_data["prediction"], out_data["ground_truth"], out_data["sql_path"])

                print(p, "===", g)
                total_correct += res

                # Log incorrect predictions
                if res == 0:
                    print(f"Incorrect Prediction {i}: {out_data['prediction']}")

            else:
                print(f"Skipping {file_path}: Missing required keys.")

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Compute final accuracy
    final_result = f"{(total_correct / num_files * 100):.2f}%" if num_files > 0 else "No valid files found"
    print(f"Final Accuracy: {final_result}")

    return final_result


def create_agent(name, description, assets, llm_id):
    """Helper function to create an agent."""
    return AgentFactory.create(
                name=name,
                description=description,
                instructions=description,
                tools=assets,
                llm_id=llm_id,
            )


def create_sql_tool(entry):
    """Helper function to create an SQL tool asset."""
    return AgentFactory.create_sql_tool(
                description=f"This is the database about {entry['db_id'].replace('_', ' ')}",
                source=rename_and_save_sqlite(entry["sql_path"]), # it has to be a .bd for an sqlite file
                source_type="sqlite",
                schema=entry["schema"], #It automatically parses the schema
                enable_commit=False,
            )

def create_python_tool():
    """Helper function to create a Python tool asset."""
    return AgentFactory.create_python_interpreter_tool()


def create_team_agent(agents, TEAM_ROLE, sql_exe, llm_id):
    """Helper function to create a team agent."""
    return TeamAgentFactory.create(
            name="Text2SQL Team Agents",
            description=TEAM_ROLE.format(exe=sql_exe),
            agents=agents,
            llm_id=llm_id,
        )

def execute_query(query, agent, team_agent, configuration, plan_inspector):
    """Execute the query with either a single agent or a team of agents."""

    if "single" in configuration:
        response = agent.run(query)
    else:
        team_agent.use_mentalist = plan_inspector if "planner" in configuration else False
        team_agent.use_inspector = plan_inspector if "inspector" in configuration else False
        if team_agent.use_inspector:
            team_agent.num_inspectors = 1
            team_agent.inspector_targets = ["steps"]   
        response = team_agent.run(query)

    return response

def safe_dump_response_step(response, result_path):
    """
    Save all intermediate steps from an Agent response into one JSON file.
    """
    try:
        steps = response.data.intermediate_steps
        serialized_steps = []

        for i, step in enumerate(steps):
            if hasattr(step, "model_dump"):
                serialized_steps.append(step.model_dump())
            elif hasattr(step, "__dict__"):
                serialized_steps.append(step.__dict__)
            else:
                serialized_steps.append(str(step))  # fallback

        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(serialized_steps, f, indent=4, ensure_ascii=False)

        print(f"[✓] Saved {len(serialized_steps)} intermediate steps to {result_path}")
    
    except Exception as e:
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump({"error": f"Failed to dump steps: {str(e)}"}, f, indent=2)
        print(f"[!] Failed to save steps: {e}")
