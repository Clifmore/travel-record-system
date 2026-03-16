"""
Formatting utilities for IDs and other data.
"""


def format_id(prefix, num):
    """
    Format ID consistently with 4-digit padding.
    
    Args:
        prefix: ID prefix (C-, A-, F-)
        num: Number to format
        
    Returns:
        str: Formatted ID (e.g., C-0001)
    """
    return f"{prefix}{num:04d}"


def get_next_id(prefix, data_dict):
    """
    Get next available ID.
    
    Args:
        prefix: ID prefix (C-, A-, F-)
        data_dict: Dictionary of existing records
        
    Returns:
        str: Next available ID
    """
    if not data_dict:
        return format_id(prefix, 1)
    existing = [int(k.split('-')[1]) for k in data_dict.keys()]
    next_num = max(existing) + 1
    return format_id(prefix, next_num)