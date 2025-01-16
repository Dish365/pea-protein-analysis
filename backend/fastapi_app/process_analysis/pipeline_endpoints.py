from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

from analytics.simulation.pipeline.workflow import AnalysisWorkflow, AnalysisType
from analytics.simulation.pipeline.scheduling import AnalysisScheduler, SchedulePriority
from analytics.simulation.pipeline.monitoring import PipelineMonitor

router = APIRouter(prefix="/pipeline", tags=["Pipeline Management"])
logger = logging.getLogger(__name__)

# Initialize components
scheduler = AnalysisScheduler()
monitor = PipelineMonitor()
workflow = AnalysisWorkflow()

# Pydantic models for request validation
class AnalysisRequest(BaseModel):
    analysis_type: str
    input_data: Dict[str, Any]
    schedule_time: Optional[datetime] = None
    priority: Optional[str] = "MEDIUM"
    repeat_interval: Optional[int] = None  # in minutes

class MonitoringTimeRange(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

@router.post("/analyze")
async def run_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Submit an analysis task for execution"""
    try:
        # Validate analysis type
        try:
            analysis_type = AnalysisType[request.analysis_type.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid analysis type. Must be one of: {[t.name for t in AnalysisType]}"
            )
        
        # If schedule_time is provided, schedule the task
        if request.schedule_time:
            try:
                priority = SchedulePriority[request.priority.upper()]
            except KeyError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid priority. Must be one of: {[p.name for p in SchedulePriority]}"
                )
            
            repeat_interval = (
                timedelta(minutes=request.repeat_interval)
                if request.repeat_interval
                else None
            )
            
            task_id = await scheduler.schedule_analysis(
                analysis_type=analysis_type.value,
                input_data=request.input_data,
                schedule_time=request.schedule_time,
                priority=priority,
                repeat_interval=repeat_interval
            )
            
            return {
                "task_id": task_id,
                "status": "scheduled",
                "schedule_time": request.schedule_time
            }
        
        # Otherwise, execute immediately
        task_id = await workflow.execute_analysis(
            analysis_type=analysis_type,
            input_data=request.input_data,
            workflow_id=None
        )
        
        return {
            "task_id": task_id,
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Error processing analysis request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a scheduled or running task"""
    try:
        scheduler.cancel_task(task_id)
        return {"status": "cancelled", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

@router.get("/monitoring/metrics")
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
        # Check if task is scheduled
        if task_id in scheduler.scheduled_tasks:
            task = scheduler.scheduled_tasks[task_id]
            return {
                "task_id": task_id,
                "status": "scheduled",
                "next_run": task.next_run,
                "last_run": task.last_run
            }
        
        # Check if task is running
        if task_id in scheduler.running_tasks:
            return {
                "task_id": task_id,
                "status": "running"
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
        for task_id, task in scheduler.scheduled_tasks.items():
            if not status or status == "scheduled":
                tasks.append({
                    "task_id": task_id,
                    "status": "scheduled",
                    "analysis_type": task.analysis_type,
                    "next_run": task.next_run,
                    "priority": task.priority
                })
        
        # Get running tasks
        for task_id in scheduler.running_tasks:
            if not status or status == "running":
                tasks.append({
                    "task_id": task_id,
                    "status": "running"
                })
        
        return {"tasks": tasks}
        
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 