from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import logging
from enum import Enum

from analytics.pipeline.orchestrator.workflow import AnalysisWorkflow
from analytics.pipeline.orchestrator.error_handling import (
    AnalysisError,
    handle_error,
    log_execution_time
)
from analytics.simulation.pipeline.scheduling import AnalysisScheduler, SchedulePriority
from analytics.simulation.pipeline.monitoring import PipelineMonitor, MetricType

router = APIRouter(prefix="/pipeline", tags=["Pipeline Management"])
logger = logging.getLogger(__name__)

# Initialize components
scheduler = AnalysisScheduler()
monitor = PipelineMonitor()
workflow = AnalysisWorkflow()

class AnalysisTypeEnum(str, Enum):
    TECHNICAL = "technical"
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental"
    ECO_EFFICIENCY = "eco_efficiency"

# Enhanced Pydantic models
class AnalysisRequest(BaseModel):
    analysis_type: AnalysisTypeEnum
    input_data: Dict[str, Any]
    schedule_time: Optional[datetime] = Field(None, description="Schedule time for delayed execution")
    priority: Optional[str] = Field("MEDIUM", description="Task priority: LOW, MEDIUM, HIGH")
    repeat_interval: Optional[int] = Field(None, description="Repeat interval in minutes")

class MonitoringTimeRange(BaseModel):
    start_time: Optional[datetime] = Field(None, description="Start time for monitoring data")
    end_time: Optional[datetime] = Field(None, description="End time for monitoring data")

@router.post("/analyze")
@log_execution_time()
async def run_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Submit an analysis task for execution"""
    try:
        # Validate priority if provided
        if request.schedule_time:
            try:
                priority = SchedulePriority[request.priority.upper()]
            except KeyError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid priority. Must be one of: {[p.name for p in SchedulePriority]}"
                )
            
            # Schedule the task
            repeat_interval = (
                timedelta(minutes=request.repeat_interval)
                if request.repeat_interval
                else None
            )
            
            task_id = await scheduler.schedule_analysis(
                analysis_type=request.analysis_type.value,
                input_data=request.input_data,
                schedule_time=request.schedule_time,
                priority=priority,
                repeat_interval=repeat_interval
            )
            
            return {
                "task_id": task_id,
                "status": "scheduled",
                "schedule_time": request.schedule_time,
                "priority": priority.name
            }
        
        # Execute immediately
        start_time = datetime.now()
        task_id = await workflow.execute_analysis(
            analysis_type=request.analysis_type,
            input_data=request.input_data,
            workflow_id=None
        )
        
        # Record task duration for monitoring
        duration = (datetime.now() - start_time).total_seconds()
        monitor.record_task_duration(task_id, duration)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "execution_time": duration
        }
        
    except AnalysisError as e:
        monitor.record_task_error(str(e))
        error_response = handle_error(e)
        raise HTTPException(status_code=500, detail=error_response)
    except Exception as e:
        monitor.record_task_error(str(e))
        logger.error(f"Error processing analysis request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a scheduled or running task"""
    try:
        scheduler.cancel_task(task_id)
        return {
            "status": "cancelled",
            "task_id": task_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error cancelling task {task_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

@router.get("/monitoring/metrics")
@log_execution_time()
async def get_metrics(timerange: MonitoringTimeRange):
    """Get performance metrics for the specified time range"""
    try:
        report = monitor.get_performance_report(
            start_time=timerange.start_time,
            end_time=timerange.end_time
        )
        return report
    except Exception as e:
        logger.error(f"Error getting monitoring metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/status/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a specific task"""
    try:
        # Check scheduled tasks
        if task_id in scheduler.scheduled_tasks:
            task = scheduler.scheduled_tasks[task_id]
            return {
                "task_id": task_id,
                "status": "scheduled",
                "analysis_type": task.analysis_type,
                "next_run": task.next_run,
                "last_run": task.last_run,
                "priority": SchedulePriority(task.priority).name
            }
        
        # Check running tasks
        if task_id in scheduler.running_tasks:
            return {
                "task_id": task_id,
                "status": "running",
                "start_time": scheduler.running_tasks[task_id].get_start_time()
            }
        
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
        
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/list")
async def list_tasks(status: Optional[str] = None):
    """List all tasks, optionally filtered by status"""
    try:
        tasks = []
        
        # Get scheduled tasks
        if not status or status == "scheduled":
            for task_id, task in scheduler.scheduled_tasks.items():
                tasks.append({
                    "task_id": task_id,
                    "status": "scheduled",
                    "analysis_type": task.analysis_type,
                    "next_run": task.next_run,
                    "last_run": task.last_run,
                    "priority": SchedulePriority(task.priority).name
                })
        
        # Get running tasks
        if not status or status == "running":
            for task_id, task in scheduler.running_tasks.items():
                tasks.append({
                    "task_id": task_id,
                    "status": "running",
                    "start_time": task.get_start_time(),
                    "analysis_type": task.get_analysis_type()
                })
        
        return {
            "tasks": tasks,
            "total_count": len(tasks),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 