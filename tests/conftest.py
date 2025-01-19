#tests/conftest.py

import pytest
import logging
from pathlib import Path
import sys
import asyncio
from typing import Generator, AsyncGenerator

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Import using relative path from tests directory
from tests.api.process_analysis.conftest import ProcessAnalysisTester

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.DEBUG)

@pytest.fixture(scope="session")
def event_loop_policy():
    """Configure event loop policy for Windows."""
    if sys.platform == 'win32':
        policy = asyncio.WindowsProactorEventLoopPolicy()
    else:
        policy = asyncio.DefaultEventLoopPolicy()
    return policy

@pytest.fixture(scope="session")
def event_loop_instance(event_loop_policy):
    """Create an instance of the event loop."""
    asyncio.set_event_loop_policy(event_loop_policy)
    loop = asyncio.new_event_loop()
    yield loop
    if not loop.is_closed():
        loop.close()

@pytest.fixture
async def process_tester():
    """Fixture providing process tester instance"""
    tester = ProcessAnalysisTester()
    yield tester
    await tester.client.aclose()