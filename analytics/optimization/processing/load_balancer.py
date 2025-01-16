import logging
from typing import List, Callable, Any
import random

logger = logging.getLogger(__name__)


class LoadBalancer:
    def __init__(self, servers: List[str]):
        self.servers = servers

    def distribute_task(self, task: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Distribute a task to a server
        """
        server = self._select_server()
        logger.info(f"Distributing task {task.__name__} to server: {server}")
        try:
            result = task(*args, **kwargs)
            logger.info(f"Task {task.__name__} completed on server: {server}")
            return result
        except Exception as e:
            logger.error(f"Task {task.__name__} failed on server: {server}: {str(e)}")
            raise

    def _select_server(self) -> str:
        """
        Select a server using a simple round-robin or random strategy
        """
        return random.choice(self.servers)
