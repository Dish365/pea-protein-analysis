import asyncio
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class AsyncHandler:
    def __init__(self):
        pass
        
    async def run_async_task(self, task: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Run an asynchronous task
        """
        try:
            result = await task(*args, **kwargs)
            logger.info(f"Task {task.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Task {task.__name__} failed: {str(e)}")
            raise
        
    async def run_concurrent_tasks(self, tasks: list) -> list:
        """
        Run multiple tasks concurrently
        """
        try:
            results = await asyncio.gather(*tasks)
            logger.info("All tasks completed successfully")
            return results
        except Exception as e:
            logger.error(f"Concurrent tasks failed: {str(e)}")
            raise 