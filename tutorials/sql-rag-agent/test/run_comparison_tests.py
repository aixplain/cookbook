#!/usr/bin/env python3
"""
Simple Test Runner for Agent vs SQL Comparison
============================================

This script runs a focused set of comparison tests between the agent and direct SQL queries.
It provides clear pass/fail results and detailed output for debugging.
"""

import sys
import os
from typing import Dict, Any, List

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import agent
from utils import DatabaseManager, ResultComparator, setup_logging


def run_test(test_name: str, agent_query: str, sql_query: str, db_manager: DatabaseManager, comparator: ResultComparator) -> bool:
    """Run a single comparison test"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Agent Query: {agent_query}")
    print(f"SQL Query: {sql_query}")
    
    try:
        # Get agent result
        print("\nRunning agent query...")
        agent_result = agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Get SQL result
        print("\nRunning SQL query...")
        sql_result = db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = comparator.compare_numeric_results(agent_result, sql_result)
        print(f"\nResults Match: {'✓ PASS' if is_match else '✗ FAIL'}")
        
        return is_match
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        return False


def main():
    """Run all comparison tests"""
    print("SQL RAG Agent vs Direct SQL Comparison Tests")
    print("=" * 60)
    
    # Setup logging and database
    logger = setup_logging()
    db_manager = DatabaseManager()
    comparator = ResultComparator(db_manager)
    
    # Define test cases
    test_cases = [
        {
            "name": "Average Age",
            "agent_query": "What is the average age of insured individuals?",
            "sql_query": "SELECT AVG(age) as average_age FROM insurance"
        },
        {
            "name": "Count of Smokers",
            "agent_query": "How many people are smokers?",
            "sql_query": "SELECT COUNT(*) as smoker_count FROM insurance WHERE smoker = 'yes'"
        },
        {
            "name": "Total Records",
            "agent_query": "What is the total number of records in the database?",
            "sql_query": "SELECT COUNT(*) as total_records FROM insurance"
        },
        {
            "name": "Average BMI",
            "agent_query": "What is the average BMI?",
            "sql_query": "SELECT AVG(bmi) as average_bmi FROM insurance"
        },
        {
            "name": "Maximum Charge",
            "agent_query": "What is the maximum insurance charge?",
            "sql_query": "SELECT MAX(charges) as max_charge FROM insurance"
        },
        {
            "name": "Minimum Charge",
            "agent_query": "What is the minimum insurance charge?",
            "sql_query": "SELECT MIN(charges) as min_charge FROM insurance"
        },
        {
            "name": "Average Charge",
            "agent_query": "What is the average insurance charge?",
            "sql_query": "SELECT AVG(charges) as average_charge FROM insurance"
        },
        {
            "name": "People with Children",
            "agent_query": "How many people have children?",
            "sql_query": "SELECT COUNT(*) as people_with_children FROM insurance WHERE children > 0"
        },
        {
            "name": "Smokers in Southeast",
            "agent_query": "How many smokers are there in the southeast region?",
            "sql_query": "SELECT COUNT(*) as smokers_southeast FROM insurance WHERE smoker = 'yes' AND region = 'southeast'"
        },
        {
            "name": "Average Age of Female Smokers",
            "agent_query": "What is the average age of female smokers?",
            "sql_query": "SELECT AVG(age) as avg_age_female_smokers FROM insurance WHERE sex = 'female' AND smoker = 'yes'"
        }
    ]
    
    # Run tests
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        success = run_test(
            test_case["name"],
            test_case["agent_query"],
            test_case["sql_query"],
            db_manager,
            comparator
        )
        if success:
            passed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")
    
    # Clean up
    db_manager.close()


if __name__ == "__main__":
    main()
