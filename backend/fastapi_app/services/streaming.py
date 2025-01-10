from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, Any
import logging
from uuid import uuid4

from . import ws_manager  # Import shared instance instead of creating new one

router = APIRouter(prefix="/stream", tags=["Real-time Streaming"])
logger = logging.getLogger(__name__)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time data streaming"""
    await ws_manager.connect(websocket, client_id)

@router.post("/alerts/configure")
async def configure_alert(config: Dict[str, Any]):
    """Configure new alert via REST endpoint"""
    try:
        await ws_manager._configure_alert(config)
        return {"status": "success", "message": "Alert configured"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics/{process_id}")
async def get_metrics(
    process_id: str,
    metric_type: str = None,
    time_range: int = 3600
):
    """Get historical metrics via REST endpoint"""
    try:
        metrics = ws_manager.dashboard.get_metrics(
            process_id=process_id,
            metric_type=metric_type,
            time_range=time_range
        )
        
        return {
            "process_id": process_id,
            "metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "value": m.value,
                    "metric_type": m.metric_type
                }
                for m in metrics
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/alerts")
async def get_alerts(
    process_id: str = None,
    time_range: int = 3600
):
    """Get historical alerts via REST endpoint"""
    try:
        alerts = ws_manager.dashboard.get_alert_history(
            process_id=process_id,
            time_range=time_range
        )
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 