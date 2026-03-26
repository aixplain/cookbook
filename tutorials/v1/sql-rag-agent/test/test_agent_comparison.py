"""
SQL RAG Agent Comparison Test Suite
==================================

This test suite compares the results from the SQL RAG agent against direct SQL queries
executed against the database. The focus is on result accuracy rather than performance.

Test Structure:
- Each test case has a natural language query for the agent
- A corresponding SQL query that should produce the same result
- Comparison logic to validate that results match (within acceptable tolerance)
"""

import unittest
import sys
import os
from typing import Dict, Any, List

# Import the agent components

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent import agent, sql_tool
from utils import DatabaseManager, ResultComparator, setup_logging


class TestAgentSQLComparison(unittest.TestCase):
    """Test cases comparing agent results with direct SQL queries"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.agent = agent
        cls.logger = setup_logging()
        cls.db_manager = DatabaseManager()
        cls.comparator = ResultComparator(cls.db_manager)
        
        # Verify database has data
        result = cls.db_manager.execute_sql("SELECT COUNT(*) as total FROM insurance")
        cls.total_records = result[0]['total']
        print(f"Database contains {cls.total_records} records")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        cls.db_manager.close()
    
    def test_01_average_age(self):
        """Test: What is the average age of insured individuals?"""
        print("\n=== Test 1: Average Age ===")
        
        # Agent query
        agent_query = "What is the average age of insured individuals?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT AVG(age) as average_age FROM insurance"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.1)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for average age")
    
    def test_02_count_smokers(self):
        """Test: How many people are smokers?"""
        print("\n=== Test 2: Count of Smokers ===")
        
        # Agent query
        agent_query = "How many people are smokers?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT COUNT(*) as smoker_count FROM insurance WHERE smoker = 'yes'"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_count_results(agent_result, sql_result)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for smoker count")
    
    def test_03_total_records(self):
        """Test: What is the total number of records in the database?"""
        print("\n=== Test 3: Total Records ===")
        
        # Agent query
        agent_query = "What is the total number of records in the database?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT COUNT(*) as total_records FROM insurance"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_count_results(agent_result, sql_result)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for total records")
    
    def test_04_unique_regions(self):
        """Test: What are the different regions in the dataset?"""
        print("\n=== Test 4: Unique Regions ===")
        
        # Agent query
        agent_query = "What are the different regions in the dataset?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT DISTINCT region FROM insurance ORDER BY region"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_list_results(agent_result, sql_result, 'region')
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for unique regions")
    
    def test_05_average_bmi(self):
        """Test: What is the average BMI?"""
        print("\n=== Test 5: Average BMI ===")
        
        # Agent query
        agent_query = "What is the average BMI?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT AVG(bmi) as average_bmi FROM insurance"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.1)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for average BMI")
    
    def test_06_maximum_charge(self):
        """Test: What is the maximum insurance charge?"""
        print("\n=== Test 6: Maximum Charge ===")
        
        # Agent query
        agent_query = "What is the maximum insurance charge?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT MAX(charges) as max_charge FROM insurance"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.01)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for maximum charge")
    
    def test_07_minimum_charge(self):
        """Test: What is the minimum insurance charge?"""
        print("\n=== Test 7: Minimum Charge ===")
        
        # Agent query
        agent_query = "What is the minimum insurance charge?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT MIN(charges) as min_charge FROM insurance"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.01)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for minimum charge")
    
    def test_08_average_charge(self):
        """Test: What is the average insurance charge?"""
        print("\n=== Test 8: Average Charge ===")
        
        # Agent query
        agent_query = "What is the average insurance charge?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT AVG(charges) as average_charge FROM insurance"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.1)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for average charge")
    
    def test_09_people_with_children(self):
        """Test: How many people have children?"""
        print("\n=== Test 9: People with Children ===")
        
        # Agent query
        agent_query = "How many people have children?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT COUNT(*) as people_with_children FROM insurance WHERE children > 0"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_count_results(agent_result, sql_result)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for people with children")
    
    def test_10_smokers_in_southeast(self):
        """Test: How many smokers are there in the southeast region?"""
        print("\n=== Test 10: Smokers in Southeast ===")
        
        # Agent query
        agent_query = "How many smokers are there in the southeast region?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT COUNT(*) as smokers_southeast FROM insurance WHERE smoker = 'yes' AND region = 'southeast'"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_count_results(agent_result, sql_result)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for smokers in southeast")
    
    def test_11_average_age_female_smokers(self):
        """Test: What is the average age of female smokers?"""
        print("\n=== Test 11: Average Age of Female Smokers ===")
        
        # Agent query
        agent_query = "What is the average age of female smokers?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT AVG(age) as avg_age_female_smokers FROM insurance WHERE sex = 'female' AND smoker = 'yes'"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.1)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for average age of female smokers")
    
    def test_12_people_more_than_2_children(self):
        """Test: How many people have more than 2 children?"""
        print("\n=== Test 12: People with More than 2 Children ===")
        
        # Agent query
        agent_query = "How many people have more than 2 children?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT COUNT(*) as people_many_children FROM insurance WHERE children > 2"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_count_results(agent_result, sql_result)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for people with more than 2 children")
    
    def test_13_average_bmi_over_50(self):
        """Test: What is the average BMI for people over 50 years old?"""
        print("\n=== Test 13: Average BMI for People Over 50 ===")
        
        # Agent query
        agent_query = "What is the average BMI for people over 50 years old?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT AVG(bmi) as avg_bmi_over_50 FROM insurance WHERE age > 50"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results with more lenient tolerance for BMI
        is_match = self.comparator.compare_numeric_results(agent_result, sql_result, tolerance=0.5)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for average BMI over 50")
    
    def test_14_charges_above_20000(self):
        """Test: How many people have charges above $20000?"""
        print("\n=== Test 14: Charges Above $20000 ===")
        
        # Agent query
        agent_query = "How many people have charges above $20000?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT COUNT(*) as high_charges FROM insurance WHERE charges > 20000"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Compare results
        is_match = self.comparator.compare_count_results(agent_result, sql_result)
        print(f"Results match: {is_match}")
        
        self.assertTrue(is_match, "Agent and SQL results should match for charges above $20000")
    
    def test_15_average_charge_by_region(self):
        """Test: What is the average charge by region?"""
        print("\n=== Test 15: Average Charge by Region ===")
        
        # Agent query
        agent_query = "What is the average charge by region?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT region, AVG(charges) as avg_charge FROM insurance GROUP BY region ORDER BY region"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # For this test, we'll check if the agent mentions all regions and reasonable values
        # This is more complex to validate exactly, so we'll do a partial validation
        regions_in_sql = [row['region'] for row in sql_result]
        print(f"Regions in SQL: {regions_in_sql}")
        
        # Extract text from AgentResponse if needed
        agent_text = agent_result.data.output if hasattr(agent_result, 'data') else str(agent_result)
        
        # Check if agent response contains region information
        agent_contains_regions = any(region.lower() in agent_text.lower() for region in regions_in_sql)
        print(f"Agent contains region info: {agent_contains_regions}")
        
        self.assertTrue(agent_contains_regions, "Agent should mention regions when asked about average charge by region")
    
    def test_16_average_bmi_by_smoking_status(self):
        """Test: What is the average BMI by smoking status?"""
        print("\n=== Test 16: Average BMI by Smoking Status ===")
        
        # Agent query
        agent_query = "What is the average BMI by smoking status?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT smoker, AVG(bmi) as avg_bmi FROM insurance GROUP BY smoker"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Extract text from AgentResponse if needed
        agent_text = agent_result.data.output if hasattr(agent_result, 'data') else str(agent_result)
        
        # Check if agent response contains smoking status information
        agent_contains_smoking = 'smoker' in agent_text.lower() or 'smoking' in agent_text.lower()
        print(f"Agent contains smoking info: {agent_contains_smoking}")
        
        self.assertTrue(agent_contains_smoking, "Agent should mention smoking status when asked about average BMI by smoking status")
    
    def test_17_total_charges_by_gender(self):
        """Test: What is the total charges by gender?"""
        print("\n=== Test 17: Total Charges by Gender ===")
        
        # Agent query
        agent_query = "What is the total charges by gender?"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT sex, SUM(charges) as total_charges FROM insurance GROUP BY sex"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Extract text from AgentResponse if needed
        agent_text = agent_result.data.output if hasattr(agent_result, 'data') else str(agent_result)
        
        # Check if agent response contains gender information
        agent_contains_gender = any(gender in agent_text.lower() for gender in ['male', 'female', 'gender'])
        print(f"Agent contains gender info: {agent_contains_gender}")
        
        self.assertTrue(agent_contains_gender, "Agent should mention gender when asked about total charges by gender")
    
    def test_18_top_5_highest_charges(self):
        """Test: Show me the top 5 highest insurance charges"""
        print("\n=== Test 18: Top 5 Highest Charges ===")
        
        # Agent query
        agent_query = "Show me the top 5 highest insurance charges"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT charges FROM insurance ORDER BY charges DESC LIMIT 5"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Extract top 5 values from SQL
        sql_top_5 = [row['charges'] for row in sql_result]
        print(f"Top 5 charges from SQL: {sql_top_5}")
        
        # Extract text from AgentResponse if needed
        agent_text = agent_result.data.output if hasattr(agent_result, 'data') else str(agent_result)
        
        # Check if agent response contains high charge values (handle formatted vs raw values)
        agent_contains_high_values = False
        for charge in sql_top_5[:3]:  # Check first 3
            # Try exact match first
            if str(charge) in agent_text:
                agent_contains_high_values = True
                break
            # Try formatted match (remove decimals and check)
            charge_int = int(charge)
            if str(charge_int) in agent_text:
                agent_contains_high_values = True
                break
            # Try with comma formatting
            charge_formatted = f"{charge:,.2f}"
            if charge_formatted in agent_text:
                agent_contains_high_values = True
                break
        
        print(f"Agent contains high charge values: {agent_contains_high_values}")
        
        self.assertTrue(agent_contains_high_values, "Agent should show high charge values when asked for top 5")
    
    def test_19_youngest_10_people(self):
        """Test: Show me the youngest 10 people in the dataset"""
        print("\n=== Test 19: Youngest 10 People ===")
        
        # Agent query
        agent_query = "Show me the youngest 10 people in the dataset"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT age FROM insurance ORDER BY age ASC LIMIT 10"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Extract youngest ages from SQL
        sql_youngest = [row['age'] for row in sql_result]
        print(f"Youngest ages from SQL: {sql_youngest}")
        
        # Extract text from AgentResponse if needed
        agent_text = agent_result.data.output if hasattr(agent_result, 'data') else str(agent_result)
        
        # Check if agent response contains young age values
        agent_contains_young_ages = any(str(age) in agent_text for age in sql_youngest[:3])  # Check first 3
        print(f"Agent contains young age values: {agent_contains_young_ages}")
        
        self.assertTrue(agent_contains_young_ages, "Agent should show young age values when asked for youngest 10")
    
    def test_20_people_with_highest_bmi(self):
        """Test: Show me the people with highest BMI"""
        print("\n=== Test 20: People with Highest BMI ===")
        
        # Agent query
        agent_query = "Show me the people with highest BMI"
        agent_result = self.agent.run(agent_query)
        print(f"Agent Result: {agent_result}")
        
        # Direct SQL query
        sql_query = "SELECT bmi FROM insurance ORDER BY bmi DESC LIMIT 10"
        sql_result = self.db_manager.execute_sql(sql_query)
        print(f"SQL Result: {sql_result}")
        
        # Extract highest BMI values from SQL
        sql_highest_bmi = [row['bmi'] for row in sql_result]
        print(f"Highest BMI values from SQL: {sql_highest_bmi}")
        
        # Extract text from AgentResponse if needed
        agent_text = agent_result.data.output if hasattr(agent_result, 'data') else str(agent_result)
        
        # Check if agent response contains high BMI values
        agent_contains_high_bmi = any(str(round(bmi, 1)) in agent_text for bmi in sql_highest_bmi[:3])  # Check first 3
        print(f"Agent contains high BMI values: {agent_contains_high_bmi}")
        
        self.assertTrue(agent_contains_high_bmi, "Agent should show high BMI values when asked for highest BMI")


def run_comparison_tests():
    """Run all comparison tests and provide summary"""
    print("SQL RAG Agent Comparison Test Suite")
    print("=" * 60)
    print("This suite compares agent results with direct SQL queries")
    print("=" * 60)
    
    # Run the tests
    unittest.main(verbosity=2, exit=False)


if __name__ == "__main__":
    run_comparison_tests()
