#tests/api/process_analysis/conftest.py

import pytest
import httpx
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ProcessAnalysisTester:
    """Base class for process analysis testing"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=30.0,
            follow_redirects=True
        )
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
    async def submit_analysis(
        self,
        test_data: Dict[str, Any],
        expected_status: int = 200
    ) -> Dict[str, Any]:
        """Submit analysis request and verify response"""
        try:
            logger.debug(f"Submitting analysis request: {test_data}")
            response = await self.client.post(
                "/api/v1/pipeline/analyze",
                json=test_data
            )
            
            if response.status_code != expected_status:
                logger.error(f"Server error response: {response.text}")
                
            assert response.status_code == expected_status, \
                f"Expected status {expected_status}, got {response.status_code}\nResponse: {response.text}"
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Analysis submission failed: {str(e)}")
            raise
            
    async def monitor_task(
        self,
        task_id: str,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Monitor task until completion or timeout"""
        start_time = datetime.now()
        while True:
            if (datetime.now() - start_time).seconds > timeout:
                raise TimeoutError(f"Task monitoring timed out after {timeout}s")
                
            response = await self.client.get(
                f"/api/v1/pipeline/tasks/status/{task_id}"
            )
            status_data = response.json()
            
            if status_data["status"] in ["completed", "failed"]:
                return status_data
                
            await asyncio.sleep(poll_interval)
            
    def save_results(self, filename: str, data: Dict[str, Any]) -> None:
        """Save test results to file"""
        file_path = self.results_dir / filename
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Results saved to {file_path}")

@pytest.fixture
async def process_tester(event_loop_instance):
    """Fixture providing process tester instance with proper cleanup"""
    async with ProcessAnalysisTester() as tester:
        yield tester

@pytest.fixture(scope="session")
async def test_server(event_loop_instance):
    """Check if server is running and ready"""
    async with httpx.AsyncClient() as client:
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                response = await client.get("http://localhost:8001/health")
                if response.status_code == 200:
                    return
                await asyncio.sleep(1)
            except httpx.ConnectError:
                if attempt == max_attempts - 1:
                    raise RuntimeError(
                        "Server is not running. Please start the server with:\n"
                        "uvicorn backend.fastapi_app.main:app --port 8001 --reload"
                    )
                await asyncio.sleep(1) 