"""
Unit tests for the SimpleAgent class in fastapi_agent.py
"""
import sys
from unittest.mock import MagicMock

# Mock dependencies that might be missing in the test environment
# This allows testing SimpleAgent in isolation
mock_fastapi = MagicMock()
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.responses"] = MagicMock()
sys.modules["pydantic"] = MagicMock()

import os
import asyncio
import pytest

# Add the parent directory to the Python path to import from scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.fastapi_agent import SimpleAgent

def test_agent_init():
    """Test SimpleAgent initialization"""
    # Test default name
    agent = SimpleAgent()
    assert agent.name == "FastAPI Agent"

    # Test custom name
    custom_name = "Test Agent"
    agent = SimpleAgent(name=custom_name)
    assert agent.name == custom_name

def test_generate_response():
    """Test synchronous response generation"""
    agent = SimpleAgent(name="TestAgent")
    query = "Hello, world!"
    response = agent.generate_response(query)

    assert isinstance(response, str)
    assert "TestAgent" in response
    assert "Hello, world!" in response
    assert "simulated agent response" in response

def test_generate_response_stream():
    """Test asynchronous streaming response generation"""
    agent = SimpleAgent(name="StreamAgent")
    query = "Stream test"

    async def collect_stream():
        tokens = []
        async for token in agent.generate_response_stream(query):
            tokens.append(token)
        return tokens

    # Use asyncio.run since pytest-asyncio might not be available
    tokens = asyncio.run(collect_stream())

    assert len(tokens) > 1
    # First token should be the prefix
    assert "StreamAgent" in tokens[0]
    assert "Stream test" in tokens[0]

    # Remaining tokens should contain the response
    full_response = "".join(tokens[1:])
    assert "simulated" in full_response
    assert "agent" in full_response
    assert "response" in full_response
