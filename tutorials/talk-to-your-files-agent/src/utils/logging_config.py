"""Centralized logging configuration for the application."""

import os
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Set up logging configuration for the application.
    
    Args:
        log_dir: Directory to store log files
        
    Returns:
        Logger instance configured for the application
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create handlers
    # Main log file - contains all logs
    main_handler = logging.handlers.RotatingFileHandler(
        log_path / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    main_handler.setFormatter(file_formatter)
    main_handler.setLevel(logging.DEBUG)
    
    # Error log file - contains only errors
    error_handler = logging.handlers.RotatingFileHandler(
        log_path / "errors.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setFormatter(file_formatter)
    error_handler.setLevel(logging.ERROR)
    
    # File operations log - tracks all file-related operations
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / "file_operations.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Create logger
    logger = logging.getLogger('file_agent')
    logger.setLevel(logging.DEBUG)
    
    # Add handlers
    logger.addHandler(main_handler)
    logger.addHandler(error_handler)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Optional name for the logger (will be prefixed with 'file_agent')
        
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f'file_agent.{name}')
    return logging.getLogger('file_agent') 