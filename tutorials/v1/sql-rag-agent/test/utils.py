"""
Test Utilities
==============

Common utilities for SQL RAG Agent comparison tests.
"""

import sqlite3
import re
import json
import logging
from typing import Dict, Any, List, Union, Optional
from pathlib import Path

from config import DATABASE_PATH, NUMERIC_TOLERANCE, COUNT_TOLERANCE, BMI_TOLERANCE


class DatabaseManager:
    """Manages database connections and queries"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DATABASE_PATH
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
    
    def execute_sql(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results as list of dictionaries"""
        if not self.conn:
            self._connect()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except sqlite3.Error as e:
            logging.error(f"SQL execution failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


class ResultComparator:
    """Compares agent results with SQL results"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def extract_numeric_value(self, text_or_response) -> Union[float, None]:
        """Extract numeric value from agent response"""
        # Handle AgentResponse object
        if hasattr(text_or_response, 'data') and hasattr(text_or_response.data, 'output'):
            text = text_or_response.data.output
        elif isinstance(text_or_response, str):
            text = text_or_response
        else:
            text = str(text_or_response)
        
        # Prioritize decimal numbers and avoid extracting age ranges
        patterns = [
            r'(\d+\.\d+)\s*(?:years?|age|charge|bmi|count|total|average|mean)',
            r'(?:is|are|equals?)\s*(\d+\.\d+)',
            r'approximately\s*(\d+\.\d+)',
            r'(\d+\.\d+)\s*(?:$|\n)',
            r'(\d+\.\d+)',  # Any decimal number
            r'(\d+)\s*(?:years?|age|charge|bmi|count|total|average|mean)',
            r'(?:is|are|equals?)\s*(\d+)',
            r'(\d+)\s*(?:$|\n)',
            r'(\d+)'  # Any integer as fallback
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    value = float(matches[0])
                    # Avoid extracting age ranges (like "over 50")
                    if value > 100 and 'over' in text.lower() and 'age' in text.lower():
                        continue
                    return value
                except ValueError:
                    continue
        return None
    
    def extract_list_values(self, text_or_response) -> List[Union[str, float]]:
        """Extract list of values from agent response"""
        # Handle AgentResponse object
        if hasattr(text_or_response, 'data') and hasattr(text_or_response.data, 'output'):
            text = text_or_response.data.output
        elif isinstance(text_or_response, str):
            text = text_or_response
        else:
            text = str(text_or_response)
        
        values = []
        
        # Try to find JSON-like arrays
        json_pattern = r'\[(.*?)\]'
        json_matches = re.findall(json_pattern, text)
        if json_matches:
            try:
                cleaned = json_matches[0].replace("'", '"')
                values = json.loads(f'[{cleaned}]')
                return values
            except:
                pass
        
        # Try to extract comma-separated values
        colon_pattern = r'(?:are|is|include|contain)[:\s]+(.*?)(?:\.|$)'
        colon_matches = re.findall(colon_pattern, text, re.IGNORECASE)
        if colon_matches:
            text = colon_matches[0]
        
        # Split by comma and clean up
        parts = text.split(',')
        for part in parts:
            part = part.strip()
            part = re.sub(r'\b(and|the|are|is|include|contain)\b', '', part, flags=re.IGNORECASE).strip()
            if part:
                try:
                    values.append(float(part))
                except ValueError:
                    values.append(part)
        
        return values
    
    def compare_numeric_results(self, agent_result, sql_result: List[Dict], 
                              tolerance: float = NUMERIC_TOLERANCE) -> bool:
        """Compare numeric results between agent and SQL"""
        agent_value = self.extract_numeric_value(agent_result)
        if agent_value is None:
            return False
        
        if not sql_result or len(sql_result) == 0:
            return False
        
        # Get the first numeric value from SQL result
        sql_value = None
        for row in sql_result:
            for value in row.values():
                if isinstance(value, (int, float)):
                    sql_value = value
                    break
            if sql_value is not None:
                break
        
        if sql_value is None:
            return False
        
        return abs(agent_value - sql_value) <= tolerance
    
    def compare_count_results(self, agent_result, sql_result: List[Dict]) -> bool:
        """Compare count results between agent and SQL"""
        agent_value = self.extract_numeric_value(agent_result)
        if agent_value is None:
            return False
        
        if not sql_result or len(sql_result) == 0:
            return False
        
        # Get the count value from SQL result
        sql_count = None
        for row in sql_result:
            for key, value in row.items():
                if 'count' in key.lower() or isinstance(value, int):
                    sql_count = value
                    break
            if sql_count is not None:
                break
        
        if sql_count is None:
            return False
        
        return int(agent_value) == int(sql_count)
    
    def compare_list_results(self, agent_result, sql_result: List[Dict], 
                           key_column: str = None) -> bool:
        """Compare list results between agent and SQL"""
        agent_values = self.extract_list_values(agent_result)
        if not agent_values:
            return False
        
        if not sql_result:
            return False
        
        # Extract values from SQL result
        sql_values = []
        for row in sql_result:
            if key_column and key_column in row:
                sql_values.append(row[key_column])
            else:
                sql_values.append(list(row.values())[0])
        
        # Convert to sets for comparison (order doesn't matter)
        agent_set = set(str(v).lower() for v in agent_values)
        sql_set = set(str(v).lower() for v in sql_values)
        
        return agent_set == sql_set


def setup_logging():
    """Setup logging configuration"""
    from config import LOG_LEVEL, LOG_FORMAT
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT
    )
    return logging.getLogger(__name__)


def get_test_database_info() -> Dict[str, Any]:
    """Get basic information about the test database"""
    db_manager = DatabaseManager()
    try:
        result = db_manager.execute_sql("SELECT COUNT(*) as total FROM insurance")
        total_records = result[0]['total']
        
        # Get sample data info
        sample_result = db_manager.execute_sql("SELECT * FROM insurance LIMIT 1")
        columns = list(sample_result[0].keys()) if sample_result else []
        
        return {
            'total_records': total_records,
            'columns': columns,
            'has_data': total_records > 0
        }
    finally:
        db_manager.close()
