from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import logging
from enum import Enum

from analytics.pipeline.orchestrator.workflow import (
    AnalysisWorkflow, 
    WorkflowType,
    WorkflowOrchestrator
)
from analytics.pipeline.orchestrator.error_handling import (
    AnalysisError,
    handle_error,
    log_execution_time,
    track_workflow_errors
)
from analytics.simulation.pipeline.scheduling import AnalysisScheduler, SchedulePriority
from analytics.simulation.pipeline.monitoring import PipelineMonitor, MetricType

router = APIRouter(tags=["Pipeline Management"])
logger = logging.getLogger(__name__)

# Initialize components
scheduler = AnalysisScheduler()
monitor = PipelineMonitor()
orchestrator = WorkflowOrchestrator()

class AnalysisTypeEnum(str, Enum):
    TECHNICAL = "technical"
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental"
    ECO_EFFICIENCY = "eco_efficiency"

class AnalysisRequest(BaseModel):
    """Analysis request model with enhanced validation"""
    workflow_type: str = Field(
        ..., 
        description="Type of workflow",
        examples=WorkflowType.values()
    )
    process_id: str = Field(..., description="Unique process identifier")
    analysis_type: AnalysisTypeEnum
    input_data: Dict[str, Any]
    schedule_time: Optional[datetime] = Field(None, description="Schedule time for delayed execution")
    priority: Optional[str] = Field("MEDIUM", description="Task priority: LOW, MEDIUM, HIGH")
    repeat_interval: Optional[int] = Field(None, description="Repeat interval in minutes")

    @validator('workflow_type')
    def validate_workflow_type(cls, v):
        try:
            return WorkflowType.from_str(v).value
        except ValueError as e:
            raise ValueError(f"Invalid workflow type: {str(e)}")

@router.post("/analyze")
@log_execution_time()
async def analyze_process(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Submit a process analysis request"""
    try:
        # Schedule task if needed
        if request.schedule_time:
            task_id = scheduler.schedule_task(
                task_data=request.dict(),
                schedule_time=request.schedule_time,
                priority=SchedulePriority[request.priority],
                repeat_interval=request.repeat_interval
            )
            return {
                "status": "scheduled",
                "task_id": task_id,
                "schedule_time": request.schedule_time.isoformat()
            }
            
        # Execute immediately using the orchestrator
        workflow_type = WorkflowType.from_str(request.workflow_type)
        results = await orchestrator.process_workflow(
            workflow_type=workflow_type,
            process_id=request.process_id,
            input_data=request.input_data
        )
        
        return {
            "status": "completed",
            "results": results,
            "execution_time": datetime.now().isoformat()
        }
        
    except AnalysisError as e:
        await track_workflow_errors(request.workflow_type, e)
        error_details = handle_error(e)
        raise HTTPException(status_code=400, detail=error_details)
    except Exception as e:
        await track_workflow_errors(request.workflow_type, e)
        logger.error(f"Analysis failed: {str(e)}")
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

class MonitoringTimeRange(BaseModel):
    """Time range for monitoring data"""
    start_time: Optional[datetime] = Field(None, description="Start time for monitoring data")
    end_time: Optional[datetime] = Field(None, description="End time for monitoring data")

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
    """Get status of a scheduled or running task"""
    try:
        status = scheduler.get_task_status(task_id)
        return {
            "task_id": task_id,
            "status": status,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting task status {task_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

@router.get("/tasks/list")
async def list_tasks():
    """List all scheduled and running tasks"""
    try:
        tasks = scheduler.list_tasks()
        return {
            "tasks": tasks,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/config")
async def get_debug_config():
    """Get current pipeline configuration for debugging"""
    try:
        return {
            "workflow_types": WorkflowType.values(),
            "analysis_types": [e.value for e in AnalysisTypeEnum],
            "priority_levels": [p.value for p in SchedulePriority],
            "metric_types": [m.value for m in MetricType],
            "scheduler_status": scheduler.get_status(),
            "monitor_status": monitor.get_status()
        }
    except Exception as e:
        logger.error(f"Error getting debug config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 