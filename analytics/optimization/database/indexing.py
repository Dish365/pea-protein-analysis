from typing import Dict, List, Any
import logging
from django.db import models, connection

logger = logging.getLogger(__name__)

class IndexManager:
    def __init__(self):
        self.index_stats = {}
        
    def analyze_table_indexes(self, model: models.Model) -> Dict[str, Any]:
        """
        Analyze indexes for a given model
        """
        meta = model._meta
        table_name = meta.db_table
        
        # Get existing indexes
        existing_indexes = self._get_existing_indexes(model)
        
        # Analyze index usage
        index_usage = self._analyze_index_usage(table_name)
        
        # Generate recommendations
        recommendations = self._generate_index_recommendations(model, existing_indexes, index_usage)
        
        return {
            "table_name": table_name,
            "existing_indexes": existing_indexes,
            "index_usage": index_usage,
            "recommendations": recommendations
        }
        
    def create_recommended_indexes(self, model: models.Model) -> List[str]:
        """
        Create recommended indexes for a model
        """
        analysis = self.analyze_table_indexes(model)
        created_indexes = []
        
        for recommendation in analysis["recommendations"]:
            if recommendation["action"] == "create":
                index_name = self._create_index(model, recommendation["fields"])
                created_indexes.append(index_name)
                
        return created_indexes
        
    def _get_existing_indexes(self, model: models.Model) -> List[Dict[str, Any]]:
        """Get existing indexes for a model"""
        indexes = []
        meta = model._meta
        
        # Get indexes from model meta
        for idx in meta.indexes:
            indexes.append({
                "name": idx.name,
                "fields": idx.fields,
                "type": "explicit"
            })
            
        # Get unique constraints
        for constraint in meta.unique_constraints:
            indexes.append({
                "name": constraint.name,
                "fields": constraint.fields,
                "type": "unique"
            })
            
        return indexes
        
    def _analyze_index_usage(self, table_name: str) -> Dict[str, Any]:
        """Analyze index usage statistics"""
        with connection.cursor() as cursor:
            # This is PostgreSQL specific - adapt for other databases
            cursor.execute("""
                SELECT
                    schemaname,
                    tablename,
                    indexname,
                    idx_scan,
                    idx_tup_read,
                    idx_tup_fetch
                FROM pg_stat_user_indexes
                WHERE tablename = %s
            """, [table_name])
            
            results = cursor.fetchall()
            
        return {
            row[2]: {  # indexname
                "scans": row[3],
                "tuples_read": row[4],
                "tuples_fetched": row[5]
            }
            for row in results
        }
        
    def _generate_index_recommendations(
        self,
        model: models.Model,
        existing_indexes: List[Dict[str, Any]],
        index_usage: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate index recommendations"""
        recommendations = []
        meta = model._meta
        
        # Check for frequently queried fields without indexes
        query_patterns = self._analyze_query_patterns(model)
        for pattern in query_patterns:
            if not self._has_matching_index(pattern["fields"], existing_indexes):
                recommendations.append({
                    "action": "create",
                    "fields": pattern["fields"],
                    "reason": f"Frequently queried fields: {', '.join(pattern['fields'])}"
                })
                
        # Check for unused indexes
        for idx in existing_indexes:
            usage = index_usage.get(idx["name"], {"scans": 0})
            if usage["scans"] == 0:
                recommendations.append({
                    "action": "consider_removing",
                    "index_name": idx["name"],
                    "reason": "Index is never used"
                })
                
        return recommendations
        
    def _analyze_query_patterns(self, model: models.Model) -> List[Dict[str, Any]]:
        """Analyze common query patterns"""
        # This would typically involve analyzing query logs or monitoring
        # For now, return basic patterns based on model structure
        patterns = []
        meta = model._meta
        
        # Add patterns for foreign key fields
        for field in meta.fields:
            if isinstance(field, models.ForeignKey):
                patterns.append({
                    "fields": [field.name],
                    "frequency": "high",
                    "type": "foreign_key"
                })
                
        return patterns
        
    def _has_matching_index(self, fields: List[str], existing_indexes: List[Dict[str, Any]]) -> bool:
        """Check if fields are covered by an existing index"""
        for idx in existing_indexes:
            if all(field in idx["fields"] for field in fields):
                return True
        return False
        
    def _create_index(self, model: models.Model, fields: List[str]) -> str:
        """Create a new index"""
        index_name = f"idx_{'_'.join(fields)}"
        index = models.Index(fields=fields, name=index_name)
        
        with connection.schema_editor() as schema_editor:
            schema_editor.add_index(model, index)
            
        return index_name 