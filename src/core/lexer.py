from tokens import Integer, Float, Operation, Declaration, Variable, Boolean, Comparison, Reserved


class Lexer:
    """
    Lexical analyzer for the Ludwig programming language.
    
    The Lexer takes raw source code text and converts it into a sequence
    of tokens that can be processed by the parser. It handles:
    - Numbers (integers and floats)
    - Operators (+, -, *, /, =, comparisons)
    - Keywords (let, if, while, etc.)
    - Variables and identifiers
    - Boolean operators (and, or, not)
    
    Example:
        >>> lexer = Lexer("let x = 42")
        >>> tokens = lexer.tokenize()
        >>> [str(token) for token in tokens]
        ['let', 'x', '=', '42']
    """
    # Language definition constants
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operations = "+-/*()="
    stopwords = [" "]
    declarations = ["let","create","start"]
    boolean = ["and", "or", "not"]
    comparisons = [">", "<", ">=", "<=", "?="]
    specialCharacters = "><=?"
    reserved = ["if", "elif", "else", "do", "while", "as"]

    def __init__(self, text):
        """
        Initialize the lexer with source code text.
        
        Args:
            text (str): The source code to tokenize
        """
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None

    def tokenize(self):
        """
        Convert the source text into a list of tokens.
        
        Returns:
            list: A list of Token objects representing the source code
        """
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()

            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()

            elif self.char in Lexer.stopwords:
                self.move()
                continue

            elif self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    self.token = Reserved(word)
                else:
                    self.token = Variable(word)

            elif self.char in Lexer.specialCharacters:
                comparisonOperator = ""
                while self.char in Lexer.specialCharacters and self.idx < len(self.text):
                    comparisonOperator += self.char
                    self.move()

                self.token = Comparison(comparisonOperator)

            self.tokens.append(self.token)

        return self.tokens

    def extract_number(self):
        """
        Extract a numeric token (integer or float) from the current position.
        
        Returns:
            Integer|Float: A numeric token
        """
        number = ""
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()

        return Integer(number) if not isFloat else Float(number)

    def extract_word(self):
        """
        Extract a word (identifier, keyword, etc.) from the current position.
        
        Returns:
            str: The extracted word
        """
        word = ""
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.move()

        return word

    def move(self):
        """Advance to the next character in the source text."""
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]

