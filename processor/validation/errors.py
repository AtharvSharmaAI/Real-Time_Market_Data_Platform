# OWNER: P2
#
# PURPOSE:
# Define validation errors.
#
# RESPONSIBILITIES:
# Error types for validation failures.

class ValidationError(Exception):
    """Base exception for validation errors."""
    pass

class MissingFieldException(ValidationError):
    """Exception raised when a required field is missing."""
    pass

class InvalidTypeException(ValidationError):
    """Exception raised when a field has an incorrect type."""
    pass

class DomainConstraintException(ValidationError):
    """Exception raised when a value violates domain constraints (e.g., price <= 0)."""
    pass
