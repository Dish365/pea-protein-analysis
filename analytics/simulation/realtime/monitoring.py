from typing import Dict, Any, List, Optional
import asyncio
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

@dataclass
class ProcessAlert:
    """Process alert configuration"""
    metric_name: str
    threshold: float
    condition: str  # 'above' or 'below'
    window_size: int  # in seconds
    alert_message: str

@dataclass
class DashboardMetric:
    """Real-time dashboard metric"""
    timestamp: datetime
    value: float
    process_id: str
    metric_type: str

class ProcessMonitoringDashboard:
    """Real-time process monitoring dashboard"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_history: Dict[str, List[DashboardMetric]] = {}
        self.active_alerts: Dict[str, ProcessAlert] = {}
        self.alert_history: List[Dict[str, Any]] = []
        self._alert_subscribers: List[asyncio.Queue] = []
        
    async def update_metrics(
        self,
        process_id: str,
        metrics: Dict[str, float]
    ):
        """Update dashboard metrics"""
        current_time = datetime.now()
        
        for metric_type, value in metrics.items():
            metric = DashboardMetric(
                timestamp=current_time,
                value=value,
                process_id=process_id,
                metric_type=metric_type
            )
            
            if process_id not in self.metrics_history:
                self.metrics_history[process_id] = []
            
            self.metrics_history[process_id].append(metric)
            
            # Check alerts for this metric
            await self._check_alerts(process_id, metric_type, value)
        
        # Cleanup old metrics
        self._cleanup_old_metrics()
    
    def add_alert(
        self,
        process_id: str,
        alert: ProcessAlert
    ):
        """Add new process alert"""
        alert_id = f"{process_id}_{alert.metric_name}"
        self.active_alerts[alert_id] = alert
        self.logger.info(f"Added alert for {alert_id}")
    
    def remove_alert(
        self,
        process_id: str,
        metric_name: str
    ):
        """Remove process alert"""
        alert_id = f"{process_id}_{metric_name}"
        if alert_id in self.active_alerts:
            del self.active_alerts[alert_id]
            self.logger.info(f"Removed alert for {alert_id}")
    
    async def subscribe_to_alerts(self) -> asyncio.Queue:
        """Subscribe to alert notifications"""
        queue = asyncio.Queue()
        self._alert_subscribers.append(queue)
        return queue
    
    async def unsubscribe_from_alerts(self, queue: asyncio.Queue):
        """Unsubscribe from alert notifications"""
        if queue in self._alert_subscribers:
            self._alert_subscribers.remove(queue)
    
    def get_metrics(
        self,
        process_id: str,
        metric_type: Optional[str] = None,
        time_range: Optional[int] = None  # in seconds
    ) -> List[DashboardMetric]:
        """Get historical metrics for specified process"""
        if process_id not in self.metrics_history:
            return []
            
        metrics = self.metrics_history[process_id]
        
        if metric_type:
            metrics = [m for m in metrics if m.metric_type == metric_type]
            
        if time_range:
            cutoff_time = datetime.now() - timedelta(seconds=time_range)
            metrics = [m for m in metrics if m.timestamp >= cutoff_time]
            
        return metrics
    
    def get_alert_history(
        self,
        process_id: Optional[str] = None,
        time_range: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get historical alerts"""
        alerts = self.alert_history
        
        if process_id:
            alerts = [a for a in alerts if a['process_id'] == process_id]
            
        if time_range:
            cutoff_time = datetime.now() - timedelta(seconds=time_range)
            alerts = [
                a for a in alerts 
                if datetime.fromisoformat(a['timestamp']) >= cutoff_time
            ]
            
        return alerts
    
    async def _check_alerts(
        self,
        process_id: str,
        metric_type: str,
        value: float
    ):
        """Check if any alerts should be triggered"""
        alert_id = f"{process_id}_{metric_type}"
        if alert_id not in self.active_alerts:
            return
            
        alert = self.active_alerts[alert_id]
        metrics = self.get_metrics(
            process_id,
            metric_type,
            alert.window_size
        )
        
        if not metrics:
            return
            
        # Calculate average over window
        avg_value = sum(m.value for m in metrics) / len(metrics)
        
        should_alert = (
            (alert.condition == 'above' and avg_value > alert.threshold) or
            (alert.condition == 'below' and avg_value < alert.threshold)
        )
        
        if should_alert:
            await self._trigger_alert(process_id, alert, avg_value)
    
    async def _trigger_alert(
        self,
        process_id: str,
        alert: ProcessAlert,
        value: float
    ):
        """Trigger alert and notify subscribers"""
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'process_id': process_id,
            'metric_name': alert.metric_name,
            'value': value,
            'threshold': alert.threshold,
            'condition': alert.condition,
            'message': alert.alert_message
        }
        
        self.alert_history.append(alert_data)
        
        # Notify subscribers
        for queue in self._alert_subscribers:
            await queue.put(alert_data)
            
        self.logger.warning(
            f"Alert triggered for {process_id} - {alert.metric_name}: {alert.alert_message}"
        )
    
    def _cleanup_old_metrics(self, max_age: int = 86400):  # 24 hours
        """Remove metrics older than max_age seconds"""
        cutoff_time = datetime.now() - timedelta(seconds=max_age)
        
        for process_id in self.metrics_history:
            self.metrics_history[process_id] = [
                m for m in self.metrics_history[process_id]
                if m.timestamp >= cutoff_time
            ] 