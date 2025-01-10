from typing import Dict, Any, List, Optional, Callable
import asyncio
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertChannel(Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"
    CONSOLE = "console"
    WEBSOCKET = "websocket"

@dataclass
class AlertRule:
    """Alert rule configuration"""
    name: str
    metric_name: str
    condition: str
    threshold: float
    severity: AlertSeverity
    channels: List[AlertChannel]
    cooldown: int  # seconds between repeated alerts
    message_template: str

@dataclass
class Alert:
    """Alert instance"""
    timestamp: datetime
    rule_name: str
    process_id: str
    metric_name: str
    value: float
    severity: AlertSeverity
    message: str

class AlertManager:
    """Manages process monitoring alerts"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alert_rules: Dict[str, AlertRule] = {}
        self.last_alerts: Dict[str, datetime] = {}
        self.alert_handlers: Dict[AlertChannel, Callable] = {}
        self._alert_history: List[Alert] = []
        
        # Register default handlers
        self._register_default_handlers()
    
    def add_rule(self, rule: AlertRule):
        """Add new alert rule"""
        self.alert_rules[rule.name] = rule
        self.logger.info(f"Added alert rule: {rule.name}")
    
    def remove_rule(self, rule_name: str):
        """Remove alert rule"""
        if rule_name in self.alert_rules:
            del self.alert_rules[rule_name]
            self.logger.info(f"Removed alert rule: {rule_name}")
    
    def register_handler(
        self,
        channel: AlertChannel,
        handler: Callable[[Alert], None]
    ):
        """Register custom alert handler"""
        self.alert_handlers[channel] = handler
        self.logger.info(f"Registered handler for channel: {channel.value}")
    
    async def process_metric(
        self,
        process_id: str,
        metric_name: str,
        value: float
    ):
        """Process metric and trigger alerts if needed"""
        for rule in self.alert_rules.values():
            if rule.metric_name != metric_name:
                continue
                
            # Check if alert is in cooldown
            last_alert = self.last_alerts.get(f"{process_id}_{rule.name}")
            if last_alert:
                cooldown_end = last_alert + timedelta(seconds=rule.cooldown)
                if datetime.now() < cooldown_end:
                    continue
            
            # Check alert condition
            should_alert = self._check_condition(rule.condition, value, rule.threshold)
            
            if should_alert:
                await self._trigger_alert(process_id, rule, value)
    
    def get_alert_history(
        self,
        process_id: Optional[str] = None,
        severity: Optional[AlertSeverity] = None,
        time_range: Optional[int] = None
    ) -> List[Alert]:
        """Get historical alerts with optional filtering"""
        alerts = self._alert_history
        
        if process_id:
            alerts = [a for a in alerts if a.process_id == process_id]
            
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
            
        if time_range:
            cutoff_time = datetime.now() - timedelta(seconds=time_range)
            alerts = [a for a in alerts if a.timestamp >= cutoff_time]
            
        return alerts
    
    def _register_default_handlers(self):
        """Register default alert handlers"""
        self.register_handler(AlertChannel.CONSOLE, self._console_handler)
        # Add other default handlers as needed
    
    def _console_handler(self, alert: Alert):
        """Default console alert handler"""
        message = (
            f"[{alert.severity.value.upper()}] {alert.timestamp.isoformat()} - "
            f"Process {alert.process_id}: {alert.message}"
        )
        if alert.severity == AlertSeverity.CRITICAL:
            self.logger.critical(message)
        elif alert.severity == AlertSeverity.WARNING:
            self.logger.warning(message)
        else:
            self.logger.info(message)
    
    def _check_condition(
        self,
        condition: str,
        value: float,
        threshold: float
    ) -> bool:
        """Check if alert condition is met"""
        if condition == "above":
            return value > threshold
        elif condition == "below":
            return value < threshold
        elif condition == "equals":
            return abs(value - threshold) < 1e-6
        return False
    
    async def _trigger_alert(
        self,
        process_id: str,
        rule: AlertRule,
        value: float
    ):
        """Trigger alert and send notifications"""
        # Create alert instance
        alert = Alert(
            timestamp=datetime.now(),
            rule_name=rule.name,
            process_id=process_id,
            metric_name=rule.metric_name,
            value=value,
            severity=rule.severity,
            message=rule.message_template.format(
                process_id=process_id,
                value=value,
                threshold=rule.threshold
            )
        )
        
        # Add to history
        self._alert_history.append(alert)
        
        # Update last alert time
        self.last_alerts[f"{process_id}_{rule.name}"] = alert.timestamp
        
        # Send notifications through configured channels
        for channel in rule.channels:
            handler = self.alert_handlers.get(channel)
            if handler:
                try:
                    await asyncio.create_task(handler(alert))
                except Exception as e:
                    self.logger.error(
                        f"Error sending alert through {channel.value}: {str(e)}"
                    ) 