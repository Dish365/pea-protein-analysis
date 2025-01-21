from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class CostTracker:
    """Tracks and analyzes cost data over time"""
    
    def __init__(self):
        self.cost_history: List[Dict[str, Any]] = []
        
    def track_costs(self, cost_data: Dict[str, Any]) -> None:
        """Add cost data to tracking history"""
        try:
            # Ensure all numeric values are floats
            sanitized_data = self._sanitize_numeric_values(cost_data)
            sanitized_data['timestamp'] = datetime.now().isoformat()
            self.cost_history.append(sanitized_data)
        except Exception as e:
            logger.error(f"Error tracking costs: {str(e)}")
            raise ValueError(f"Failed to track costs: {str(e)}")

    def _sanitize_numeric_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively convert all numeric values to float"""
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result[key] = self._sanitize_numeric_values(value)
            elif isinstance(value, (int, float, str)):
                try:
                    result[key] = float(value)
                except (ValueError, TypeError):
                    result[key] = value
            else:
                result[key] = value
        return result

    def get_cost_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """Get summary of tracked costs within date range"""
        try:
            filtered_costs = self._filter_by_date_range(start_date, end_date)
            
            summary = defaultdict(float)
            for entry in filtered_costs:
                self._aggregate_costs(entry, summary)
            
            return dict(summary)
        except Exception as e:
            logger.error(f"Error getting cost summary: {str(e)}")
            raise ValueError(f"Failed to get cost summary: {str(e)}")

    def _filter_by_date_range(
        self,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Dict[str, Any]]:
        """Filter cost history by date range"""
        if not (start_date or end_date):
            return self.cost_history
            
        filtered = []
        for entry in self.cost_history:
            entry_date = datetime.fromisoformat(entry['timestamp'])
            if start_date and entry_date < start_date:
                continue
            if end_date and entry_date > end_date:
                continue
            filtered.append(entry)
        return filtered

    def _aggregate_costs(self, cost_data: Dict[str, Any], summary: Dict[str, float]) -> None:
        """Recursively aggregate costs from nested structure"""
        for key, value in cost_data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        summary[f"{key}_{sub_key}"] += float(sub_value)
            elif isinstance(value, (int, float)):
                summary[key] += float(value)

    def get_cost_trends(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get cost trends over time"""
        try:
            trends = defaultdict(list)
            for entry in self.cost_history:
                timestamp = entry.get('timestamp')
                if not timestamp:
                    continue
                    
                self._extract_trends(entry, timestamp, trends)
            
            return dict(trends)
        except Exception as e:
            logger.error(f"Error getting cost trends: {str(e)}")
            raise ValueError(f"Failed to get cost trends: {str(e)}")

    def _extract_trends(
        self,
        data: Dict[str, Any],
        timestamp: str,
        trends: Dict[str, List[Dict[str, Any]]]
    ) -> None:
        """Extract trend data from cost entry"""
        for key, value in data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        trends[f"{key}_{sub_key}"].append({
                            "timestamp": timestamp,
                            "value": float(sub_value)
                        })
            elif isinstance(value, (int, float)):
                trends[key].append({
                    "timestamp": timestamp,
                    "value": float(value)
                })
