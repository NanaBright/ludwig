"""
Ludwig Interactive Shell

A REPL (Read-Eval-Print Loop) for the Ludwig programming language.
Provides an interactive environment for testing Ludwig code.
"""

from core.lexer import Lexer
from core.parse import Parser
from core.interpreter import Interpreter
from core.data import Data
import sys


class LudwigShell:
    """Interactive shell for Ludwig programming language."""
    
    def __init__(self):
        """Initialize the Ludwig shell."""
        self.data = Data()
        self.version = "0.1.0-alpha"
    
    def show_banner(self):
        """Display the Ludwig welcome banner."""
        print("=" * 50)
        print(f"Ludwig Programming Language v{self.version}")
        print("Laravel-inspired features for Python-like syntax")
        print("=" * 50)
        print("Type 'help' for assistance or 'exit' to quit")
        print()
    
    def show_help(self):
        """Display help information."""
        help_text = """
Ludwig Shell Commands:
  help          - Show this help message
  exit, quit    - Exit the shell
  clear         - Clear all variables
  vars          - Show all variables
  version       - Show Ludwig version

Ludwig Syntax:
  let x = 42                    # Variable declaration
  let result = 10 + 5 * 2      # Arithmetic
  let name = "Ludwig"          # String (future feature)
  
  if x > 10 do                 # Conditional
      let status = "large"
  else do
      let status = "small"
  
  let i = 0                    # Loop
  while i < 5 do
      let i = i + 1

Operators:
  +, -, *, /      # Arithmetic
  >, <, >=, <=    # Comparison
  ?=              # Equality
  and, or, not    # Boolean

Declaration keywords: let, create, start
        """
        print(help_text)
    
    def execute_command(self, text):
        """
        Execute a Ludwig command or shell command.
        
        Args:
            text (str): Command to execute
            
        Returns:
            bool: True to continue, False to exit
        """
        text = text.strip()
        
        # Handle shell commands
        if text in ['exit', 'quit']:
            print("Goodbye!")
            return False
        elif text == 'help':
            self.show_help()
            return True
        elif text == 'clear':
            self.data = Data()
            print("Variables cleared.")
            return True
        elif text == 'vars':
            variables = self.data.read_all()
            if variables:
                print("Variables:")
                for name, value in variables.items():
                    print(f"  {name} = {value} ({value.type})")
            else:
                print("No variables defined.")
            return True
        elif text == 'version':
            print(f"Ludwig v{self.version}")
            return True
        elif text == '':
            return True
        
        # Execute Ludwig code
        try:
            tokenizer = Lexer(text)
            tokens = tokenizer.tokenize()
            
            if not tokens:
                return True
            
            parser = Parser(tokens)
            tree = parser.parse()
            
            interpreter = Interpreter(tree, self.data)
            result = interpreter.interpret()
            
            if result is not None:
                if hasattr(result, 'type') and hasattr(result, 'value'):
                    print(f"{result.value} ({result.type})")
                else:
                    print(result)
                    
        except IndexError:
            print("Error: Incomplete expression")
        except AttributeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        
        return True
    
    def run(self):
        """Run the interactive shell."""
        self.show_banner()
        
        while True:
            try:
                text = input("Ludwig> ")
                if not self.execute_command(text):
                    break
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit Ludwig shell.")
            except EOFError:
                print("\nGoodbye!")
                break


# Legacy support for existing shell usage
base = Data()

def main():
    """Main entry point for the Ludwig shell."""
    shell = LudwigShell()
    shell.run()


if __name__ == "__main__":
    main()
else:
    # Provide the old interface for backwards compatibility
    def interactive_mode():
        """Legacy interactive mode function."""
        main()
    
    # Original shell loop for backwards compatibility
    if len(sys.argv) == 1:  # If run as module
        while True:
            text = input("LudWig: ")

            tokenizer = Lexer(text)
            tokens = tokenizer.tokenize()

            parser = Parser(tokens)
            tree = parser.parse()

            interpreter = Interpreter(tree, base)
            result = interpreter.interpret()
            if result is not None:
                print(result)
