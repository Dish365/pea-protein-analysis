from typing import List, Dict, Optional
from datetime import datetime
from django.db import transaction
from ..models import BaselineProcess, RFTreatmentProcess, IRTreatmentProcess

class BatchProcessor:
    """
    Handle batch processing operations for different process types.
    
    Features:
    --------
    1. Batch Creation
    2. Parallel Processing
    3. Status Tracking
    4. Error Handling
    
    Integration:
    -----------
    - Links with FastAPI calculation services
    - Uses shared validation logic
    - Maintains process history
    """
    
    def __init__(self):
        self.process_models = {
            'baseline': BaselineProcess,
            'rf': RFTreatmentProcess,
            'ir': IRTreatmentProcess
        }
        
    @transaction.atomic
    def create_batch(
        self,
        process_type: str,
        batch_data: List[Dict],
        batch_id: str
    ) -> Dict:
        """Create a new process batch with multiple steps."""
        if process_type not in self.process_models:
            raise ValueError(f"Unknown process type: {process_type}")
            
        model_class = self.process_models[process_type]
        batch_records = []
        
        try:
            for step_data in batch_data:
                step_data['process_id'] = f"{batch_id}_{len(batch_records)}"
                record = model_class.objects.create(**step_data)
                batch_records.append(record)
                
            return {
                'batch_id': batch_id,
                'process_type': process_type,
                'steps_created': len(batch_records),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            # Rollback happens automatically due to @transaction.atomic
            raise ValueError(f"Batch creation failed: {str(e)}")
    
    def process_batch(
        self,
        batch_id: str,
        calculation_service: Any
    ) -> Dict:
        """
        Process a batch and calculate results.
        
        Integration with FastAPI:
        - Uses shared calculation service
        - Maintains consistent data format
        - Ensures validation across systems
        """
        results = {
            'batch_id': batch_id,
            'steps': [],
            'summary': {}
        }
        
        # Get all records for this batch
        for process_type, model in self.process_models.items():
            batch_records = model.objects.filter(
                process_id__startswith=f"{batch_id}_"
            ).order_by('timestamp')
            
            if batch_records.exists():
                for record in batch_records:
                    # Convert model instance to dict
                    step_data = {
                        field.name: getattr(record, field.name)
                        for field in record._meta.fields
                    }
                    
                    # Calculate step results using FastAPI service
                    step_results = calculation_service.calculate_performance_metrics(
                        step_data,
                        self._get_target_values(process_type)
                    )
                    
                    results['steps'].append({
                        'step_id': record.process_id,
                        'data': step_data,
                        'results': step_results
                    })
                
                # Calculate batch summary
                results['summary'] = self._calculate_batch_summary(results['steps'])
                break
                
        return results
    
    def _get_target_values(self, process_type: str) -> Dict[str, float]:
        """Get target values for process type."""
        targets = {
            'baseline': {
                'protein_content': 65.0,
                'yield': 85.0
            },
            'rf': {
                'moisture_content': 12.0,
                'energy_efficiency': 90.0
            },
            'ir': {
                'surface_temperature': 120.0,
                'moisture_content': 10.0
            }
        }
        return targets.get(process_type, {})
    
    def _calculate_batch_summary(self, steps: List[Dict]) -> Dict:
        """Calculate summary metrics for the batch."""
        if not steps:
            return {}
            
        # Extract performance metrics
        performances = [
            step['results'].get('overall_performance', 0)
            for step in steps
        ]
        
        return {
            'average_performance': sum(performances) / len(performances),
            'total_steps': len(steps),
            'completion_time': steps[-1]['data']['timestamp']
        } 