from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
import numpy as np
from dataclasses import dataclass

@dataclass
class ProcessMetrics:
    """Real-time process metrics"""
    timestamp: datetime
    protein_yield: float
    separation_efficiency: float
    energy_consumption: float
    temperature: float
    moisture_content: float
    particle_size: float

class RealTimeProcessor:
    """Handles real-time process calculations and monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_metrics: Dict[str, ProcessMetrics] = {}
        self._subscribers: List[asyncio.Queue] = []
        
    async def process_data(
        self,
        process_id: str,
        data: Dict[str, Any]
    ) -> ProcessMetrics:
        """Process incoming real-time data"""
        try:
            # Calculate process metrics
            metrics = ProcessMetrics(
                timestamp=datetime.now(),
                protein_yield=self._calculate_protein_yield(data),
                separation_efficiency=self._calculate_separation_efficiency(data),
                energy_consumption=data.get('energy_consumption', 0.0),
                temperature=data.get('temperature', 0.0),
                moisture_content=data.get('moisture_content', 0.0),
                particle_size=self._calculate_particle_size(data)
            )
            
            # Update current metrics
            self.current_metrics[process_id] = metrics
            
            # Notify subscribers
            await self._notify_subscribers(process_id, metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error processing real-time data: {str(e)}")
            raise
    
    def _calculate_protein_yield(self, data: Dict[str, Any]) -> float:
        """Calculate real-time protein yield"""
        input_protein = data.get('input_protein_content', 0.0)
        output_protein = data.get('output_protein_content', 0.0)
        input_mass = data.get('input_mass', 0.0)
        output_mass = data.get('output_mass', 0.0)
        
        if input_mass <= 0 or input_protein <= 0:
            return 0.0
            
        return (output_protein * output_mass) / (input_protein * input_mass) * 100
    
    def _calculate_separation_efficiency(self, data: Dict[str, Any]) -> float:
        """Calculate real-time separation efficiency"""
        protein_recovery = data.get('protein_recovery', 0.0)
        purity = data.get('protein_purity', 0.0)
        
        return protein_recovery * purity / 100
    
    def _calculate_particle_size(self, data: Dict[str, Any]) -> float:
        """Calculate real-time particle size distribution"""
        particle_sizes = data.get('particle_sizes', [])
        if not particle_sizes:
            return 0.0
            
        return np.median(particle_sizes)
    
    async def subscribe(self) -> asyncio.Queue:
        """Subscribe to real-time updates"""
        queue = asyncio.Queue()
        self._subscribers.append(queue)
        return queue
    
    async def unsubscribe(self, queue: asyncio.Queue):
        """Unsubscribe from real-time updates"""
        if queue in self._subscribers:
            self._subscribers.remove(queue)
    
    async def _notify_subscribers(self, process_id: str, metrics: ProcessMetrics):
        """Notify subscribers of new metrics"""
        message = {
            "process_id": process_id,
            "metrics": {
                "timestamp": metrics.timestamp.isoformat(),
                "protein_yield": metrics.protein_yield,
                "separation_efficiency": metrics.separation_efficiency,
                "energy_consumption": metrics.energy_consumption,
                "temperature": metrics.temperature,
                "moisture_content": metrics.moisture_content,
                "particle_size": metrics.particle_size
            }
        }
        
        for queue in self._subscribers:
            await queue.put(message) 