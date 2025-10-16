"""
Test Configuration
==================

Centralized configuration for SQL RAG Agent comparison tests.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Database configuration
DATABASE_PATH = PROJECT_ROOT / "insurance.db"

# Test tolerances
NUMERIC_TOLERANCE = 0.1
COUNT_TOLERANCE = 0
BMI_TOLERANCE = 0.5

# Test settings
VERBOSE_OUTPUT = True
SAVE_FAILED_TESTS = True
MAX_RETRIES = 3

# Agent settings
AGENT_TIMEOUT = 30  # seconds

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
