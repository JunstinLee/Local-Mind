# Backend/api/routers/filter_utils.py

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

def build_where_clause(filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Constructs a ChromaDB 'where' clause from the frontend filter selection.
    """
    if not filters:
        return None

    and_conditions = []

    # --- File Type Filter ---
    file_types = filters.get('fileType')
    if file_types:
        # Assuming metadata stores file extension without a dot, e.g., 'log'
        processed_types = [f"{t.lower()}" for t in file_types]
        and_conditions.append({"file_extension": {"$in": processed_types}})

    # --- Modification Time Filter ---
    modified_date = filters.get('modifiedDate')
    if modified_date and modified_date != 'any':
        now = datetime.now()
        if modified_date == 'day':
            start_time = now - timedelta(days=1)
        elif modified_date == 'week':
            start_time = now - timedelta(weeks=1)
        elif modified_date == 'month':
            start_time = now - timedelta(days=30) # Approximation
        else:
            start_time = None
        
        if start_time:
            # Assuming metadata stores timestamp as unix timestamp
            and_conditions.append({"last_modified": {"$gte": start_time.timestamp()}})

    # --- File Size Filter ---
    file_size = filters.get('fileSize')
    if file_size and file_size != 'any':
        size_conditions = {}
        if file_size == 's': # < 1MB
            size_conditions["$lt"] = 1024 * 1024
        elif file_size == 'm': # 1MB - 10MB
            size_conditions["$gte"] = 1024 * 1024
            size_conditions["$lte"] = 10 * 1024 * 1024
        elif file_size == 'l': # > 10MB
            size_conditions["$gt"] = 10 * 1024 * 1024
        
        if size_conditions:
            and_conditions.append({"file_size": size_conditions})

    # --- Date Range Filter (Example, assuming 'creation_date') ---
    date_range = filters.get('dateRange')
    if date_range and date_range != 'all':
        now = datetime.now()
        if date_range == 'today':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range == 'week':
            start_time = now - timedelta(days=now.weekday())
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range == 'month':
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif date_range == 'year':
            start_time = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_time = None

        if start_time:
            # Assuming metadata stores timestamp as unix timestamp
            and_conditions.append({"creation_date": {"$gte": start_time.timestamp()}})


    if not and_conditions:
        return None

    if len(and_conditions) == 1:
        return and_conditions[0]

    return {"$and": and_conditions}