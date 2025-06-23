"""
Ludwig Validation - Laravel-inspired validation system

Provides a simple, fluent API for validating data in Ludwig programs.
Inspired by Laravel's validation system but adapted for Ludwig's syntax.
"""

class ValidationError(Exception):
    """Exception raised when validation fails."""
    
    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors or {}
        super().__init__(self.message)


class Validator:
    """
    Data validation class for Ludwig.
    
    Provides methods to validate various data types and formats.
    Can be used to validate user input, function parameters, etc.
    
    Example usage:
        validator = Validator()
        result = validator.validate(data, rules)
        if not result.is_valid():
            print("Validation failed:", result.errors())
    """
    
    def __init__(self):
        """Initialize the validator."""
        self.errors = {}
    
    def validate(self, data, rules):
        """
        Validate data against a set of rules.
        
        Args:
            data (dict): Data to validate
            rules (dict): Validation rules
            
        Returns:
            ValidationResult: Result of validation
        """
        self.errors = {}
        
        for field, rule_list in rules.items():
            if field not in data:
                if 'required' in rule_list:
                    self.add_error(field, f"{field} is required")
                continue
            
            value = data[field]
            
            for rule in rule_list:
                if not self.apply_rule(field, value, rule):
                    break
        
        return ValidationResult(self.errors)
    
    def apply_rule(self, field, value, rule):
        """
        Apply a single validation rule to a field.
        
        Args:
            field (str): Field name
            value: Field value
            rule (str): Validation rule
            
        Returns:
            bool: True if validation passes
        """
        if rule == 'required':
            return self.required(field, value)
        elif rule == 'integer':
            return self.integer(field, value)
        elif rule == 'float':
            return self.float(field, value)
        elif rule == 'string':
            return self.string(field, value)
        elif rule == 'boolean':
            return self.boolean(field, value)
        elif rule.startswith('min:'):
            min_val = int(rule.split(':')[1])
            return self.min_length(field, value, min_val)
        elif rule.startswith('max:'):
            max_val = int(rule.split(':')[1])
            return self.max_length(field, value, max_val)
        elif rule.startswith('between:'):
            min_val, max_val = map(int, rule.split(':')[1].split(','))
            return self.between(field, value, min_val, max_val)
        elif rule == 'email':
            return self.email(field, value)
        elif rule.startswith('in:'):
            allowed = rule.split(':')[1].split(',')
            return self.in_list(field, value, allowed)
        else:
            self.add_error(field, f"Unknown validation rule: {rule}")
            return False
    
    def required(self, field, value):
        """Check if field has a value."""
        if value is None or value == "":
            self.add_error(field, f"{field} is required")
            return False
        return True
    
    def integer(self, field, value):
        """Check if value is an integer."""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            self.add_error(field, f"{field} must be an integer")
            return False
    
    def float(self, field, value):
        """Check if value is a float."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            self.add_error(field, f"{field} must be a number")
            return False
    
    def string(self, field, value):
        """Check if value is a string."""
        if not isinstance(value, str):
            self.add_error(field, f"{field} must be a string")
            return False
        return True
    
    def boolean(self, field, value):
        """Check if value is a boolean."""
        if not isinstance(value, bool):
            self.add_error(field, f"{field} must be true or false")
            return False
        return True
    
    def min_length(self, field, value, min_val):
        """Check if value meets minimum length."""
        if len(str(value)) < min_val:
            self.add_error(field, f"{field} must be at least {min_val} characters")
            return False
        return True
    
    def max_length(self, field, value, max_val):
        """Check if value doesn't exceed maximum length."""
        if len(str(value)) > max_val:
            self.add_error(field, f"{field} must not exceed {max_val} characters")
            return False
        return True
    
    def between(self, field, value, min_val, max_val):
        """Check if numeric value is between min and max."""
        try:
            num_value = float(value)
            if not (min_val <= num_value <= max_val):
                self.add_error(field, f"{field} must be between {min_val} and {max_val}")
                return False
            return True
        except (ValueError, TypeError):
            self.add_error(field, f"{field} must be a number")
            return False
    
    def email(self, field, value):
        """Check if value is a valid email format."""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, str(value)):
            self.add_error(field, f"{field} must be a valid email address")
            return False
        return True
    
    def in_list(self, field, value, allowed):
        """Check if value is in allowed list."""
        if str(value) not in allowed:
            self.add_error(field, f"{field} must be one of: {', '.join(allowed)}")
            return False
        return True
    
    def add_error(self, field, message):
        """Add an error message for a field."""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)


class ValidationResult:
    """
    Result of a validation operation.
    
    Contains validation status and any error messages.
    """
    
    def __init__(self, errors):
        """
        Initialize validation result.
        
        Args:
            errors (dict): Validation errors
        """
        self.validation_errors = errors
    
    def is_valid(self):
        """
        Check if validation passed.
        
        Returns:
            bool: True if no errors
        """
        return len(self.validation_errors) == 0
    
    def errors(self):
        """
        Get validation errors.
        
        Returns:
            dict: Validation errors by field
        """
        return self.validation_errors
    
    def first_error(self):
        """
        Get the first error message.
        
        Returns:
            str: First error message or None
        """
        for field_errors in self.validation_errors.values():
            if field_errors:
                return field_errors[0]
        return None
    
    def has_error(self, field):
        """
        Check if a specific field has errors.
        
        Args:
            field (str): Field name
            
        Returns:
            bool: True if field has errors
        """
        return field in self.validation_errors and len(self.validation_errors[field]) > 0


# Helper functions for use in Ludwig
def validate(data, rules):
    """
    Validate data against rules.
    
    Args:
        data (dict): Data to validate
        rules (dict): Validation rules
        
    Returns:
        ValidationResult: Validation result
    """
    validator = Validator()
    return validator.validate(data, rules)


def is_valid(data, rules):
    """
    Check if data is valid against rules.
    
    Args:
        data (dict): Data to validate
        rules (dict): Validation rules
        
    Returns:
        bool: True if valid
    """
    return validate(data, rules).is_valid()


# Example usage and tests
if __name__ == "__main__":
    # Test validation
    data = {
        'name': 'John Doe',
        'age': 25,
        'email': 'john@example.com',
        'role': 'admin'
    }
    
    rules = {
        'name': ['required', 'string', 'min:2'],
        'age': ['required', 'integer', 'between:18,100'],
        'email': ['required', 'email'],
        'role': ['required', 'in:admin,user,guest']
    }
    
    result = validate(data, rules)
    print("Validation result:", "PASSED" if result.is_valid() else "FAILED")
    
    if not result.is_valid():
        print("Errors:", result.errors())
    
    # Test with invalid data
    invalid_data = {
        'name': '',
        'age': 'not_a_number',
        'email': 'invalid_email',
        'role': 'unknown'
    }
    
    result2 = validate(invalid_data, rules)
    print("\nInvalid data result:", "PASSED" if result2.is_valid() else "FAILED")
    print("Errors:", result2.errors())
