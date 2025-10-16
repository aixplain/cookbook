#!/usr/bin/env python3
"""
Demo Script: Agent vs SQL Comparison
===============================

This script demonstrates how to compare agent results with direct SQL queries.
It shows a simple example with detailed output for learning purposes.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent import agent
from utils import DatabaseManager, ResultComparator, setup_logging


def demo_comparison():
    """Demonstrate agent vs SQL comparison"""
    print("SQL RAG Agent vs Direct SQL Comparison Demo")
    print("=" * 50)
    
    # Setup logging and database
    logger = setup_logging()
    db_manager = DatabaseManager()
    comparator = ResultComparator(db_manager)
    
    # Example 1: Average Age
    print("\n1. AVERAGE AGE COMPARISON")
    print("-" * 30)
    
    # Agent query
    print("Asking agent: 'What is the average age of insured individuals?'")
    agent_result = agent.run("What is the average age of insured individuals?")
    print(f"Agent response: {agent_result}")
    
    # Direct SQL
    print("\nRunning direct SQL: SELECT AVG(age) FROM insurance")
    sql_result = db_manager.execute_sql("SELECT AVG(age) as avg_age FROM insurance")
    sql_age = sql_result[0]['avg_age'] if sql_result else None
    print(f"SQL result: {sql_age}")
    
    # Compare
    agent_age = comparator.extract_numeric_value(agent_result)
    
    print(f"\nComparison:")
    print(f"  Agent extracted: {agent_age}")
    print(f"  SQL result: {sql_age}")
    print(f"  Difference: {abs(agent_age - sql_age) if agent_age and sql_age else 'N/A'}")
    print(f"  Match: {'✓ YES' if comparator.compare_numeric_results(agent_result, sql_result) else '✗ NO'}")
    
    # Example 2: Count of Smokers
    print("\n\n2. COUNT OF SMOKERS COMPARISON")
    print("-" * 30)
    
    # Agent query
    print("Asking agent: 'How many people are smokers?'")
    agent_result = agent.run("How many people are smokers?")
    print(f"Agent response: {agent_result}")
    
    # Direct SQL
    print("\nRunning direct SQL: SELECT COUNT(*) FROM insurance WHERE smoker = 'yes'")
    sql_result = db_manager.execute_sql("SELECT COUNT(*) as smoker_count FROM insurance WHERE smoker = 'yes'")
    sql_count = sql_result[0]['smoker_count'] if sql_result else None
    print(f"SQL result: {sql_count}")
    
    # Compare
    agent_count = comparator.extract_numeric_value(agent_result)
    
    print(f"\nComparison:")
    print(f"  Agent extracted: {agent_count}")
    print(f"  SQL result: {sql_count}")
    print(f"  Match: {'✓ YES' if comparator.compare_count_results(agent_result, sql_result) else '✗ NO'}")
    
    # Example 3: Maximum Charge
    print("\n\n3. MAXIMUM CHARGE COMPARISON")
    print("-" * 30)
    
    # Agent query
    print("Asking agent: 'What is the maximum insurance charge?'")
    agent_result = agent.run("What is the maximum insurance charge?")
    print(f"Agent response: {agent_result}")
    
    # Direct SQL
    print("\nRunning direct SQL: SELECT MAX(charges) FROM insurance")
    sql_result = db_manager.execute_sql("SELECT MAX(charges) as max_charge FROM insurance")
    sql_charge = sql_result[0]['max_charge'] if sql_result else None
    print(f"SQL result: {sql_charge}")
    
    # Compare
    agent_charge = comparator.extract_numeric_value(agent_result)
    
    print(f"\nComparison:")
    print(f"  Agent extracted: {agent_charge}")
    print(f"  SQL result: {sql_charge}")
    print(f"  Difference: {abs(agent_charge - sql_charge) if agent_charge and sql_charge else 'N/A'}")
    print(f"  Match: {'✓ YES' if comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.01) else '✗ NO'}")
    
    # Summary
    print("\n\nSUMMARY")
    print("=" * 50)
    print("This demo shows how to:")
    print("1. Run agent queries")
    print("2. Execute direct SQL queries")
    print("3. Extract numeric values from agent responses")
    print("4. Compare results with tolerance")
    print("\nFor automated testing, use:")
    print("- run_comparison_tests.py (simple)")
    print("- test_agent_comparison.py (comprehensive)")
    
    # Clean up
    db_manager.close()


if __name__ == "__main__":
    demo_comparison()
