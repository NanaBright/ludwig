class Token:
    """
    Base token class for the Ludwig programming language.
    
    All tokens in Ludwig inherit from this base class, providing
    a consistent interface for type identification and value storage.
    
    Attributes:
        type (str): The token type identifier
        value (str|int|float): The actual value of the token
    """
    def __init__(self, type, value):
        """
        Initialize a new token.
        
        Args:
            type (str): The token type (e.g., 'INT', 'FLT', 'OP')
            value: The token's value
        """
        self.type = type
        self.value = value

    def __repr__(self):
        """Return string representation of the token's value."""
        return str(self.value)


class Integer(Token):
    """Token representing integer literals in Ludwig."""
    def __init__(self, value):
        """Initialize an integer token."""
        super().__init__("INT", value)


class Float(Token):
    """Token representing floating-point literals in Ludwig."""
    def __init__(self, value):
        """Initialize a float token."""
        super().__init__("FLT", value)


class Operation(Token):
    """Token representing arithmetic and assignment operators."""
    def __init__(self, value):
        """Initialize an operation token."""
        super().__init__("OP", value)


class Declaration(Token):
    """Token representing variable declaration keywords (let, create, start)."""
    def __init__(self, value):
        """Initialize a declaration token."""
        super().__init__("DECL", value)


class Variable(Token):
    """Token representing variable identifiers."""
    def __init__(self, value):
        """Initialize a variable token."""
        super().__init__("VAR(?)", value)
        # Variable name, VAR, data type
        # let a = 5 # VAR(?)


class Boolean(Token):
    """Token representing boolean operators (and, or, not)."""
    def __init__(self, value):
        """Initialize a boolean token."""
        super().__init__("BOOL", value)


class Comparison(Token):
    """Token representing comparison operators (>, <, >=, <=, ?=)."""
    def __init__(self, value):
        """Initialize a comparison token."""
        super().__init__("COMP", value)


class Reserved(Token):
    """Token representing reserved keywords (if, elif, else, do, while, as)."""
    def __init__(self, value):
        """Initialize a reserved keyword token."""
        super().__init__("RSV", value)
