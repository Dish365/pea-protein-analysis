from typing import Dict, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
import logging
import json
import asyncio
from datetime import datetime

from analytics.simulation.realtime.processing import RealTimeProcessor
from analytics.simulation.realtime.monitoring import ProcessMonitoringDashboard
from analytics.simulation.realtime.alerting import AlertManager, AlertChannel

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manages WebSocket connections and real-time data streaming"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.processor = RealTimeProcessor()
        self.dashboard = ProcessMonitoringDashboard()
        self.alert_manager = AlertManager()
        
        # Register WebSocket alert handler
        self.alert_manager.register_handler(
            AlertChannel.WEBSOCKET,
            self._broadcast_alert
        )
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Handle new WebSocket connection"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")
        
        try:
            # Subscribe to alerts
            alert_queue = await self.dashboard.subscribe_to_alerts()
            
            # Start listening for messages and sending updates
            await asyncio.gather(
                self._listen_for_messages(websocket, client_id),
                self._send_updates(websocket, client_id, alert_queue)
            )
            
        except WebSocketDisconnect:
            await self.disconnect(client_id)
        except Exception as e:
            logger.error(f"WebSocket error for client {client_id}: {str(e)}")
            await self.disconnect(client_id)
    
    async def disconnect(self, client_id: str):
        """Handle WebSocket disconnection"""
        if client_id in self.active_connections:
            await self.active_connections[client_id].close()
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")
    
    async def _listen_for_messages(self, websocket: WebSocket, client_id: str):
        """Listen for incoming WebSocket messages"""
        try:
            while True:
                message = await websocket.receive_json()
                await self._handle_message(client_id, message)
                
        except WebSocketDisconnect:
            raise
        except Exception as e:
            logger.error(f"Error processing message from {client_id}: {str(e)}")
            raise
    
    async def _send_updates(
        self,
        websocket: WebSocket,
        client_id: str,
        alert_queue: asyncio.Queue
    ):
        """Send real-time updates to client"""
        try:
            while True:
                # Wait for alerts
                alert = await alert_queue.get()
                
                # Send update
                await websocket.send_json({
                    "type": "alert",
                    "data": alert
                })
                
        except WebSocketDisconnect:
            raise
        except Exception as e:
            logger.error(f"Error sending updates to {client_id}: {str(e)}")
            raise
    
    async def _handle_message(self, client_id: str, message: Dict[str, Any]):
        """Handle incoming WebSocket message"""
        try:
            message_type = message.get("type")
            data = message.get("data", {})
            
            if message_type == "process_data":
                # Handle real-time process data
                process_id = data.get("process_id")
                metrics = await self.processor.process_data(process_id, data)
                await self.dashboard.update_metrics(process_id, metrics.__dict__)
                
            elif message_type == "subscribe_metrics":
                # Handle metric subscription
                process_id = data.get("process_id")
                metric_types = data.get("metric_types", [])
                await self._send_metrics_update(client_id, process_id, metric_types)
                
            elif message_type == "configure_alert":
                # Handle alert configuration
                await self._configure_alert(data)
                
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            if client_id in self.active_connections:
                await self.active_connections[client_id].send_json({
                    "type": "error",
                    "data": {"message": str(e)}
                })
    
    async def _broadcast_alert(self, alert: Dict[str, Any]):
        """Broadcast alert to all connected clients"""
        message = {
            "type": "alert",
            "data": alert
        }
        
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error sending alert to {client_id}: {str(e)}")
    
    async def _send_metrics_update(
        self,
        client_id: str,
        process_id: str,
        metric_types: list
    ):
        """Send metrics update to specific client"""
        if client_id not in self.active_connections:
            return
            
        websocket = self.active_connections[client_id]
        metrics = {}
        
        for metric_type in metric_types:
            metric_data = self.dashboard.get_metrics(
                process_id=process_id,
                metric_type=metric_type,
                time_range=3600  # Last hour
            )
            metrics[metric_type] = [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "value": m.value
                }
                for m in metric_data
            ]
        
        await websocket.send_json({
            "type": "metrics_update",
            "data": {
                "process_id": process_id,
                "metrics": metrics
            }
        })
    
    async def _configure_alert(self, config: Dict[str, Any]):
        """Configure new alert from WebSocket message"""
        process_id = config.get("process_id")
        metric_name = config.get("metric_name")
        threshold = config.get("threshold")
        condition = config.get("condition", "above")
        window_size = config.get("window_size", 300)  # 5 minutes default
        
        if not all([process_id, metric_name, threshold]):
            raise ValueError("Missing required alert configuration parameters")
            
        alert = self.dashboard.ProcessAlert(
            metric_name=metric_name,
            threshold=float(threshold),
            condition=condition,
            window_size=int(window_size),
            alert_message=(
                f"Process {process_id}: {metric_name} is {condition} "
                f"threshold {threshold}"
            )
        )
        
        self.dashboard.add_alert(process_id, alert) 