from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio
import logging
from uuid import uuid4
from enum import Enum
from dataclasses import dataclass

@dataclass
class ScheduledAnalysis:
    """Represents a scheduled analysis task"""
    id: str
    analysis_type: str
    input_data: Dict[str, Any]
    schedule_time: datetime
    priority: int
    repeat_interval: Optional[timedelta] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None

class SchedulePriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class AnalysisScheduler:
    """Manages scheduling of analysis tasks"""
    
    def __init__(self):
        self.scheduled_tasks: Dict[str, ScheduledAnalysis] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.logger = logging.getLogger(__name__)
        
    async def schedule_analysis(
        self,
        analysis_type: str,
        input_data: Dict[str, Any],
        schedule_time: datetime,
        priority: SchedulePriority = SchedulePriority.MEDIUM,
        repeat_interval: Optional[timedelta] = None
    ) -> str:
        """Schedule a new analysis task"""
        task_id = str(uuid4())
        
        scheduled_task = ScheduledAnalysis(
            id=task_id,
            analysis_type=analysis_type,
            input_data=input_data,
            schedule_time=schedule_time,
            priority=priority.value,
            repeat_interval=repeat_interval,
            next_run=schedule_time
        )
        
        self.scheduled_tasks[task_id] = scheduled_task
        self.logger.info(f"Scheduled analysis task {task_id} for {schedule_time}")
        
        return task_id
    
    async def start_scheduler(self):
        """Start the scheduler loop"""
        while True:
            try:
                await self._process_scheduled_tasks()
                await asyncio.sleep(1)  # Check every second
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {str(e)}")
    
    async def _process_scheduled_tasks(self):
        """Process scheduled tasks"""
        current_time = datetime.now()
        
        # Get tasks that need to be run
        pending_tasks = [
            task for task in self.scheduled_tasks.values()
            if task.next_run and task.next_run <= current_time
        ]
        
        # Sort by priority
        pending_tasks.sort(key=lambda x: x.priority, reverse=True)
        
        for task in pending_tasks:
            if task.id not in self.running_tasks:
                # Start task
                self.running_tasks[task.id] = asyncio.create_task(
                    self._execute_task(task)
                )
                
                # Update next run time if recurring
                if task.repeat_interval:
                    task.last_run = current_time
                    task.next_run = current_time + task.repeat_interval
                else:
                    # Remove one-time tasks from schedule
                    self.scheduled_tasks.pop(task.id, None)
    
    async def _execute_task(self, task: ScheduledAnalysis):
        """Execute a scheduled task"""
        try:
            from .workflow import AnalysisWorkflow
            workflow = AnalysisWorkflow()
            
            self.logger.info(f"Starting scheduled task {task.id}")
            result = await workflow.execute_analysis(
                task.analysis_type,
                task.input_data,
                task.id
            )
            
            self.logger.info(f"Completed scheduled task {task.id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing task {task.id}: {str(e)}")
            raise
        finally:
            # Cleanup
            self.running_tasks.pop(task.id, None)
    
    def cancel_task(self, task_id: str):
        """Cancel a scheduled task"""
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks.pop(task_id)
            self.logger.info(f"Cancelled scheduled task {task_id}")
            
        if task_id in self.running_tasks:
            self.running_tasks[task_id].cancel()
            self.logger.info(f"Cancelled running task {task_id}") 