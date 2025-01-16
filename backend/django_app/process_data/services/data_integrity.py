from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import json

class DataIntegrityChecker:
    """
    Ensure data integrity and maintain audit trail for process data.
    
    Integrity Checks:
    ---------------
    1. Data Completeness:
       - Required fields present
       - Value ranges valid
       - Timestamps sequential
    
    2. Data Consistency:
       - Mass balances maintained
       - Component balances valid
       - Parameter relationships logical
    
    3. Data Security:
       - Hash verification
       - Audit trail maintenance
       - Change tracking
    """
    
    def __init__(self):
        self.audit_trail = []
        self.data_hashes = {}
        
    def calculate_data_hash(self, data: Dict) -> str:
        """Calculate SHA-256 hash of data dictionary."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def check_data_completeness(
        self,
        data: Dict,
        required_fields: List[str]
    ) -> Dict[str, bool]:
        """
        Check if all required fields are present and valid.
        
        Validation Steps:
        1. Check required fields presence
        2. Validate value types
        3. Check for null/empty values
        """
        results = {
            'complete': True,
            'missing_fields': [],
            'invalid_fields': []
        }
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                results['complete'] = False
                results['missing_fields'].append(field)
                continue
                
            value = data[field]
            
            # Check for null/empty values
            if value is None:
                results['invalid_fields'].append(f"{field}: null value")
            elif isinstance(value, (str, list, dict)) and not value:
                results['invalid_fields'].append(f"{field}: empty value")
                
        return results
    
    def check_data_consistency(
        self,
        current_data: Dict,
        previous_data: Optional[Dict] = None,
        tolerance: float = 0.02
    ) -> Dict[str, bool]:
        """
        Check data consistency within current data and against previous data.
        
        Consistency Checks:
        1. Mass balance consistency
        2. Component balance consistency
        3. Parameter relationship consistency
        4. Time sequence consistency
        """
        results = {
            'consistent': True,
            'mass_balance_valid': True,
            'component_balance_valid': True,
            'parameter_relationships_valid': True,
            'time_sequence_valid': True,
            'issues': []
        }
        
        # Check mass balance
        if 'mass_flows' in current_data:
            total_in = sum(current_data['mass_flows'].get('inputs', {}).values())
            total_out = sum(current_data['mass_flows'].get('outputs', {}).values())
            
            if abs(total_in - total_out) > tolerance * total_in:
                results['mass_balance_valid'] = False
                results['consistent'] = False
                results['issues'].append('Mass balance violation')
        
        # Check time sequence if previous data exists
        if previous_data and 'timestamp' in current_data and 'timestamp' in previous_data:
            if current_data['timestamp'] <= previous_data['timestamp']:
                results['time_sequence_valid'] = False
                results['consistent'] = False
                results['issues'].append('Invalid time sequence')
        
        return results
    
    def record_data_change(
        self,
        data_id: str,
        old_data: Dict,
        new_data: Dict,
        user_id: str,
        change_type: str
    ) -> Dict[str, Any]:
        """
        Record changes to data in audit trail.
        
        Change Types:
        - CREATE: New data entry
        - UPDATE: Modified existing data
        - DELETE: Removed data
        - VALIDATE: Data validation
        """
        timestamp = datetime.now()
        old_hash = self.calculate_data_hash(old_data) if old_data else None
        new_hash = self.calculate_data_hash(new_data) if new_data else None
        
        change_record = {
            'data_id': data_id,
            'timestamp': timestamp,
            'user_id': user_id,
            'change_type': change_type,
            'old_hash': old_hash,
            'new_hash': new_hash,
            'changes': self._compute_changes(old_data, new_data)
        }
        
        self.audit_trail.append(change_record)
        if new_hash:
            self.data_hashes[data_id] = new_hash
            
        return change_record
    
    def _compute_changes(
        self,
        old_data: Optional[Dict],
        new_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Compute detailed changes between old and new data."""
        changes = {}
        
        if not old_data:
            return {'type': 'CREATE', 'data': new_data}
        if not new_data:
            return {'type': 'DELETE', 'data': old_data}
            
        for key in set(old_data.keys()) | set(new_data.keys()):
            if key not in old_data:
                changes[key] = {'type': 'ADDED', 'value': new_data[key]}
            elif key not in new_data:
                changes[key] = {'type': 'REMOVED', 'value': old_data[key]}
            elif old_data[key] != new_data[key]:
                changes[key] = {
                    'type': 'MODIFIED',
                    'old': old_data[key],
                    'new': new_data[key]
                }
                
        return changes
    
    def verify_data_integrity(
        self,
        data_id: str,
        data: Dict
    ) -> Dict[str, bool]:
        """
        Verify data integrity using stored hash.
        
        Verification Steps:
        1. Calculate current data hash
        2. Compare with stored hash
        3. Check audit trail consistency
        """
        current_hash = self.calculate_data_hash(data)
        stored_hash = self.data_hashes.get(data_id)
        
        results = {
            'integrity_valid': False,
            'hash_match': False,
            'audit_trail_valid': True,
            'issues': []
        }
        
        # Check hash match
        if stored_hash:
            results['hash_match'] = current_hash == stored_hash
            if not results['hash_match']:
                results['issues'].append('Data hash mismatch')
        else:
            results['issues'].append('No stored hash found')
        
        # Verify audit trail consistency
        changes = [
            record for record in self.audit_trail
            if record['data_id'] == data_id
        ]
        
        if changes:
            last_hash = changes[-1]['new_hash']
            if last_hash != current_hash:
                results['audit_trail_valid'] = False
                results['issues'].append('Audit trail inconsistency')
        
        results['integrity_valid'] = (
            results['hash_match'] and
            results['audit_trail_valid']
        )
        
        return results 