# SQL RAG Agent Comparison Tests

This directory contains test cases that compare the SQL RAG agent's results against direct SQL queries executed against the database.

## Quick Start

### 1. Run Simple Comparison Tests
```bash
python run_comparison_tests.py
```
This runs 10 key test cases with clear pass/fail results.

### 2. Run Comprehensive Tests
```bash
python test_agent_comparison.py
```
This runs 20+ detailed test cases with advanced comparison logic.

### 3. See Demo
```bash
python demo_comparison.py
```
This shows a step-by-step example of how the comparison works.

## Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| `run_comparison_tests.py` | Simple test runner | Quick validation, debugging |
| `test_agent_comparison.py` | Comprehensive test suite | Full testing, CI/CD |
| `demo_comparison.py` | Educational demo | Learning how it works |
| `config.py` | Test configuration | Settings and tolerances |
| `utils.py` | Common utilities | Shared functionality |

## What These Tests Do

1. **Ask the agent** a natural language question
2. **Execute the equivalent SQL** directly against the database
3. **Compare the results** to ensure they match
4. **Report pass/fail** for each test case

## Example Test Flow

```
Question: "What is the average age?"
↓
Agent Response: "The average age is 39.2 years"
↓
Direct SQL: SELECT AVG(age) FROM insurance
SQL Result: 39.207
↓
Comparison: 39.2 ≈ 39.207 ✓ PASS
```

## Test Categories

- **Basic Aggregations**: Average, count, sum, min, max
- **Filtering**: Conditional queries with WHERE clauses
- **Grouping**: GROUP BY operations
- **Complex Queries**: Multi-condition filtering

## Requirements

- SQLite database at `insurance.db` (relative to project root)
- aixplain agent properly configured with API key
- Python packages: sqlite3, re, unittest, pathlib

## Configuration

Test settings can be modified in `config.py`:
- Database path
- Numeric tolerances
- Logging levels
- Timeout settings

## Troubleshooting

### Agent Not Responding
- Check API key in `agent.py`
- Verify agent initialization
- Check network connection

### Results Don't Match
- Check if agent generated correct SQL
- Verify database has expected data
- Review tolerance settings in `config.py`

### Tests Failing
- Run `demo_comparison.py` first
- Check individual SQL queries manually
- Verify agent understands questions

## Success Criteria

A test passes when:
- Agent executes without errors
- Agent produces a result
- Result contains expected numeric value
- Value matches SQL result within tolerance

## Customizing Tests

To add your own test cases, modify the test files and add entries like:

```python
{
    "name": "Your Test Name",
    "agent_query": "Your natural language question",
    "sql_query": "SELECT your_sql_query"
}
```

## Architecture

The test suite uses a modular architecture:
- `config.py`: Centralized configuration
- `utils.py`: Common utilities and database management
- Test files: Focus on test logic, not infrastructure

## Performance Notes

- Tests focus on accuracy, not speed
- Each test takes 5-30 seconds
- Full suite takes 10-15 minutes
- Use simple runner for faster feedback

