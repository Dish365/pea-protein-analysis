from typing import Dict, List, Any, Optional
import logging
from django.db.models import QuerySet
from django.db import connection

logger = logging.getLogger(__name__)

class QueryOptimizer:
    def __init__(self):
        self.query_cache = {}
        
    def optimize_query(self, queryset: QuerySet, hints: Optional[Dict[str, Any]] = None) -> QuerySet:
        """
        Optimize a Django queryset based on provided hints
        """
        if hints is None:
            hints = {}
            
        queryset = self._optimize_relations(queryset, hints)
        queryset = self._optimize_field_selection(queryset, hints)
        queryset = self._apply_caching(queryset, hints)
        
        return queryset
        
    def _optimize_relations(self, queryset: QuerySet, hints: Dict[str, Any]) -> QuerySet:
        """Optimize related field fetching"""
        select_related_fields = self._get_select_related_fields(queryset, hints)
        prefetch_related_fields = self._get_prefetch_related_fields(queryset, hints)
        
        if select_related_fields:
            queryset = queryset.select_related(*select_related_fields)
            
        if prefetch_related_fields:
            queryset = queryset.prefetch_related(*prefetch_related_fields)
            
        return queryset
        
    def _optimize_field_selection(self, queryset: QuerySet, hints: Dict[str, Any]) -> QuerySet:
        """Optimize field selection"""
        needed_fields = hints.get("needed_fields", [])
        if needed_fields:
            queryset = queryset.only(*needed_fields)
            
        deferred_fields = hints.get("deferred_fields", [])
        if deferred_fields:
            queryset = queryset.defer(*deferred_fields)
            
        return queryset
        
    def _apply_caching(self, queryset: QuerySet, hints: Dict[str, Any]) -> QuerySet:
        """Apply caching strategies"""
        cache_key = hints.get("cache_key")
        cache_timeout = hints.get("cache_timeout", 300)  # 5 minutes default
        
        if cache_key:
            cached_result = self.query_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
                
            result = list(queryset)  # Execute query
            self.query_cache[cache_key] = result
            return result
            
        return queryset
        
    def _get_select_related_fields(self, queryset: QuerySet, hints: Dict[str, Any]) -> List[str]:
        """Determine fields for select_related"""
        model = queryset.model
        fields = []
        
        # Check model fields for foreign keys
        for field in model._meta.fields:
            if field.is_relation and not field.many_to_many:
                fields.append(field.name)
                
        # Add hints-specified fields
        hint_fields = hints.get("select_related", [])
        fields.extend(hint_fields)
        
        return list(set(fields))  # Remove duplicates
        
    def _get_prefetch_related_fields(self, queryset: QuerySet, hints: Dict[str, Any]) -> List[str]:
        """Determine fields for prefetch_related"""
        model = queryset.model
        fields = []
        
        # Check model fields for many-to-many relationships
        for field in model._meta.many_to_many:
            fields.append(field.name)
            
        # Add hints-specified fields
        hint_fields = hints.get("prefetch_related", [])
        fields.extend(hint_fields)
        
        return list(set(fields))  # Remove duplicates 