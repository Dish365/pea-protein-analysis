from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import asyncio
from dataclasses import dataclass
from enum import Enum
import psutil
import json

class MetricType(Enum):
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    TASK_DURATION = "task_duration"
    ERROR_RATE = "error_rate"
    TASK_QUEUE_SIZE = "task_queue_size"

@dataclass
class PerformanceMetric:
    """Represents a performance metric measurement"""
    metric_type: MetricType
    value: float
    timestamp: datetime
    task_id: Optional[str] = None
    
@dataclass
class AlertConfig:
    """Configuration for performance alerts"""
    metric_type: MetricType
    threshold: float
    window_size: timedelta
    alert_interval: timedelta
    last_alert: Optional[datetime] = None

class PipelineMonitor:
    """Monitors analysis pipeline performance and resource usage"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.alerts: List[AlertConfig] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize default alerts
        self._setup_default_alerts()
    
    def _setup_default_alerts(self):
        """Setup default monitoring alerts"""
        self.alerts = [
            AlertConfig(
                metric_type=MetricType.CPU_USAGE,
                threshold=80.0,  # 80% CPU usage
                window_size=timedelta(minutes=5),
                alert_interval=timedelta(minutes=15)
            ),
            AlertConfig(
                metric_type=MetricType.MEMORY_USAGE,
                threshold=85.0,  # 85% memory usage
                window_size=timedelta(minutes=5),
                alert_interval=timedelta(minutes=15)
            ),
            AlertConfig(
                metric_type=MetricType.ERROR_RATE,
                threshold=5.0,  # 5% error rate
                window_size=timedelta(minutes=30),
                alert_interval=timedelta(minutes=30)
            )
        ]
    
    async def start_monitoring(self):
        """Start the monitoring loop"""
        while True:
            try:
                await self._collect_metrics()
                await self._check_alerts()
                await asyncio.sleep(60)  # Collect metrics every minute
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
    
    async def _collect_metrics(self):
        """Collect current performance metrics"""
        current_time = datetime.now()
        
        # Collect CPU usage
        cpu_metric = PerformanceMetric(
            metric_type=MetricType.CPU_USAGE,
            value=psutil.cpu_percent(),
            timestamp=current_time
        )
        self.metrics.append(cpu_metric)
        
        # Collect memory usage
        memory = psutil.virtual_memory()
        memory_metric = PerformanceMetric(
            metric_type=MetricType.MEMORY_USAGE,
            value=memory.percent,
            timestamp=current_time
        )
        self.metrics.append(memory_metric)
        
        # Cleanup old metrics
        self._cleanup_old_metrics()
    
    def _cleanup_old_metrics(self, max_age: timedelta = timedelta(hours=24)):
        """Remove metrics older than max_age"""
        cutoff_time = datetime.now() - max_age
        self.metrics = [
            metric for metric in self.metrics
            if metric.timestamp > cutoff_time
        ]
    
    async def _check_alerts(self):
        """Check metrics against alert thresholds"""
        current_time = datetime.now()
        
        for alert in self.alerts:
            # Skip if alert was recently sent
            if (alert.last_alert and 
                current_time - alert.last_alert < alert.alert_interval):
                continue
            
            # Get relevant metrics within window
            window_start = current_time - alert.window_size
            relevant_metrics = [
                metric for metric in self.metrics
                if (metric.metric_type == alert.metric_type and
                    metric.timestamp > window_start)
            ]
            
            if relevant_metrics:
                avg_value = sum(m.value for m in relevant_metrics) / len(relevant_metrics)
                
                if avg_value > alert.threshold:
                    self._send_alert(alert, avg_value)
                    alert.last_alert = current_time
    
    def _send_alert(self, alert: AlertConfig, value: float):
        """Send alert for threshold violation"""
        message = (
            f"Alert: {alert.metric_type.value} exceeded threshold "
            f"({value:.1f}% > {alert.threshold}%)"
        )
        self.logger.warning(message)
        # Implement additional alert notifications (email, Slack, etc.)
    
    def record_task_duration(self, task_id: str, duration: float):
        """Record the duration of a completed task"""
        metric = PerformanceMetric(
            metric_type=MetricType.TASK_DURATION,
            value=duration,
            timestamp=datetime.now(),
            task_id=task_id
        )
        self.metrics.append(metric)
    
    def record_task_error(self, task_id: str):
        """Record a task error"""
        metric = PerformanceMetric(
            metric_type=MetricType.ERROR_RATE,
            value=1.0,
            timestamp=datetime.now(),
            task_id=task_id
        )
        self.metrics.append(metric)
    
    def get_performance_report(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate a performance report for the specified time period"""
        if not start_time:
            start_time = datetime.now() - timedelta(hours=24)
        if not end_time:
            end_time = datetime.now()
            
        relevant_metrics = [
            metric for metric in self.metrics
            if start_time <= metric.timestamp <= end_time
        ]
        
        report = {
            "period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            },
            "metrics": {},
            "task_statistics": self._calculate_task_statistics(relevant_metrics)
        }
        
        # Calculate statistics for each metric type
        for metric_type in MetricType:
            metrics_of_type = [
                m for m in relevant_metrics
                if m.metric_type == metric_type
            ]
            
            if metrics_of_type:
                values = [m.value for m in metrics_of_type]
                report["metrics"][metric_type.value] = {
                    "average": sum(values) / len(values),
                    "max": max(values),
                    "min": min(values)
                }
        
        return report
    
    def _calculate_task_statistics(
        self,
        metrics: List[PerformanceMetric]
    ) -> Dict[str, Any]:
        """Calculate statistics about task execution"""
        task_durations = [
            m for m in metrics
            if m.metric_type == MetricType.TASK_DURATION
        ]
        
        task_errors = [
            m for m in metrics
            if m.metric_type == MetricType.ERROR_RATE
        ]
        
        return {
            "total_tasks": len(task_durations),
            "average_duration": (
                sum(m.value for m in task_durations) / len(task_durations)
                if task_durations else 0
            ),
            "error_count": len(task_errors),
            "error_rate": (
                len(task_errors) / len(task_durations) * 100
                if task_durations else 0
            )
        } 