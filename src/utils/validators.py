"""
Validation functions for form inputs.
"""

import re


def validate_email(email):
    """
    Comprehensive email validation accepting all valid formats.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    email = email.strip()
    
    # Basic checks
    if not email:
        return False
    
    # Must have exactly one @
    if email.count('@') != 1:
        return False
    
    # Split into local and domain
    local, domain = email.split('@')
    
    # Local part checks
    if not local or len(local) > 64:
        return False
    
    # Domain checks
    if not domain or len(domain) > 255:
        return False
    
    # Domain must have at least one dot
    if '.' not in domain:
        return False
    
    # Check domain parts
    domain_parts = domain.split('.')
    if len(domain_parts) < 2:
        return False
    
    # Each domain part must be non-empty and valid
    for part in domain_parts:
        if not part:
            return False
        # Can't start or end with hyphen
        if part.startswith('-') or part.endswith('-'):
            return False
        # Can only contain letters, numbers, hyphens
        if not re.match(r'^[a-zA-Z0-9-]+$', part):
            return False
    
    # Last part (TLD) must be at least 2 characters
    if len(domain_parts[-1]) < 2:
        return False
    
    return True