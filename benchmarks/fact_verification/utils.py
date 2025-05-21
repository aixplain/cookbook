import os
import json
import ast
from typing import List, Tuple, Optional, Union
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score, classification_report, confusion_matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


import re
import ast
import json
from typing import List, Union

def extract_classifications(answer_list: List[Union[str, dict]]) -> List[int]:
    """
    Extract classification labels (0, 1, 2, or 4) from various answer formats:
    - Markdown-wrapped JSON (```json ... ```)
    - JSON strings with double quotes
    - Python-style dict strings with single quotes
    - Native Python dictionaries
    """

    def clean_and_parse(item: str) -> Union[dict, str]:
        """Clean markdown fences and try JSON or Python-style parsing."""
        # Remove markdown-style fences
        item = re.sub(r'^```(?:json)?\s*|\s*```$', '', item.strip(), flags=re.IGNORECASE)

        # Try parsing as JSON (first choice)
        try:
            return json.loads(item)
        except json.JSONDecodeError:
            pass

        # Try parsing as Python dict
        try:
            return ast.literal_eval(item)
        except Exception:
            return item  # Return original if both fail

    def extract_from_dict(item: dict) -> int:
        """Extract classification from known key paths."""
        key_paths = [
            ("classification",),
            ("query", "classification"),
            ("Claim Analysis", "Evidence Assessment"),
            ("claim_analysis", "evidence_classification"),
        ]
        for path in key_paths:
            ref = item
            for key in path:
                if isinstance(ref, dict) and key in ref:
                    ref = ref[key]
                else:
                    break
            else:  # only if the full path was followed
                try:
                    return int(ref)
                except (ValueError, TypeError):
                    return 4
        return 4

    classifications = []
    for item in answer_list:
        # If it's a string, try to parse it
        if isinstance(item, str):
            item = clean_and_parse(item)

        # If it's a dict, try to extract classification
        if isinstance(item, dict):
            label = extract_from_dict(item)
        else:
            label = 4  # unclassifiable

        classifications.append(label)

    return classifications


def calculate_accuracy(true_labels, predicted_labels):
    accuracy = accuracy_score(true_labels, predicted_labels)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    return accuracy

def calculate_metrics(true_labels, predicted_labels):
    # Calculate accuracy
    accuracy = accuracy_score(true_labels, predicted_labels)
    
    # Calculate F1-score
    f1 = f1_score(true_labels, predicted_labels, average='weighted')
    
    # Get detailed classification report
    report = classification_report(true_labels, predicted_labels, zero_division=1)
    
    # Calculate confusion matrix
    cm = confusion_matrix(true_labels, predicted_labels)
    
    # Create confusion matrix visualization
    plt.figure(figsize=(10,8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
    
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"F1-Score: {f1:.4f}")
    print("\nDetailed Classification Report:")
    print(report)
    
    return accuracy, f1


def save_predictions(data_val, file_name="predict_val.csv", column="New Column"):
    """
    Save or update predictions in a CSV file, adding a new column each time.

    Parameters:
        data_val (list): The data to be saved as a new column.
        file_name (str): The name of the CSV file.
        column (str): The name of the column to add.
    """
    if os.path.exists(file_name):
        # Load the existing file
        df_output = pd.read_csv(file_name)
        if len(df_output) != len(data_val):
            raise ValueError(f"Length of new column ({len(data_val)}) does not match existing rows ({len(df_output)}).")
            
        # Add the new column
        df_output[column] = data_val
        print(f"Added column '{column}' to existing file '{file_name}'.")
    else:
        # Create a new DataFrame with the data
        df_output = pd.DataFrame(data_val, columns=[column])
        print(f"File '{file_name}' created with column '{column}'.")

    # Save the updated DataFrame back to the CSV file
    df_output.to_csv(file_name, index=False)
    
    
def safe_dump_response_step(response, result_path):
    """Save all intermediate steps from an Agent response into one JSON file."""
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
        


