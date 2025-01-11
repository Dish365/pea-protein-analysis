from typing import Dict, List
from datetime import datetime

class CostTracker:
    def __init__(self):
        self.cost_history = []
        
    def track_costs(self, costs: Dict[str, float], timestamp: datetime = None) -> None:
        """
        Track costs with timestamp for historical analysis.
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        self.cost_history.append({
            "timestamp": timestamp,
            "costs": costs
        })
    
    def get_cost_summary(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, float]:
        """
        Get summary of costs within specified date range.
        """
        filtered_costs = self.cost_history
        if start_date:
            filtered_costs = [c for c in filtered_costs if c["timestamp"] >= start_date]
        if end_date:
            filtered_costs = [c for c in filtered_costs if c["timestamp"] <= end_date]
            
        if not filtered_costs:
            return {}
            
        # Initialize summary with first cost entry's keys
        summary = {k: 0.0 for k in filtered_costs[0]["costs"].keys()}
        
        # Sum up all costs
        for entry in filtered_costs:
            for cost_type, amount in entry["costs"].items():
                summary[cost_type] += amount
                
        # Add total
        summary["total"] = sum(v for k, v in summary.items() if k != "total")
        
        return summary
    
    def get_cost_trends(self, cost_type: str = None) -> List[Dict[str, float]]:
        """
        Get historical cost trends for analysis.
        """
        if not self.cost_history:
            return []
            
        trends = []
        for entry in self.cost_history:
            trend_entry = {
                "timestamp": entry["timestamp"],
                "total": sum(entry["costs"].values())
            }
            if cost_type and cost_type in entry["costs"]:
                trend_entry[cost_type] = entry["costs"][cost_type]
            trends.append(trend_entry)
            
        return trends
