"""
Ludwig Collections - Laravel-inspired collection utilities

Provides a fluent, convenient wrapper for working with arrays of data.
Inspired by Laravel's Collection class but adapted for Ludwig's syntax.
"""

class Collection:
    """
    A fluent wrapper around arrays that provides helpful methods
    for filtering, mapping, and manipulating data.
    
    Example usage in Ludwig:
        let numbers = [1, 2, 3, 4, 5]
        let collection = Collection(numbers)
        let doubled = collection.map(lambda x: x * 2)
        let filtered = collection.filter(lambda x: x > 2)
    """
    
    def __init__(self, items=None):
        """
        Initialize a new collection.
        
        Args:
            items (list): Initial items for the collection
        """
        self.items = items or []
    
    def all(self):
        """
        Get all items in the collection.
        
        Returns:
            list: All items in the collection
        """
        return self.items
    
    def count(self):
        """
        Get the number of items in the collection.
        
        Returns:
            int: Number of items
        """
        return len(self.items)
    
    def first(self, default=None):
        """
        Get the first item in the collection.
        
        Args:
            default: Default value if collection is empty
            
        Returns:
            The first item or default value
        """
        return self.items[0] if self.items else default
    
    def last(self, default=None):
        """
        Get the last item in the collection.
        
        Args:
            default: Default value if collection is empty
            
        Returns:
            The last item or default value
        """
        return self.items[-1] if self.items else default
    
    def push(self, item):
        """
        Add an item to the end of the collection.
        
        Args:
            item: Item to add
            
        Returns:
            Collection: Self for method chaining
        """
        self.items.append(item)
        return self
    
    def pop(self):
        """
        Remove and return the last item from the collection.
        
        Returns:
            The removed item
        """
        return self.items.pop() if self.items else None
    
    def filter(self, callback=None):
        """
        Filter the collection using a callback function.
        
        Args:
            callback (function): Function to test each item
            
        Returns:
            Collection: New filtered collection
        """
        if callback is None:
            # Filter out falsy values
            filtered = [item for item in self.items if item]
        else:
            filtered = [item for item in self.items if callback(item)]
        
        return Collection(filtered)
    
    def map(self, callback):
        """
        Transform each item in the collection using a callback.
        
        Args:
            callback (function): Function to transform each item
            
        Returns:
            Collection: New collection with transformed items
        """
        mapped = [callback(item) for item in self.items]
        return Collection(mapped)
    
    def reduce(self, callback, initial=None):
        """
        Reduce the collection to a single value.
        
        Args:
            callback (function): Function to reduce items
            initial: Initial value for reduction
            
        Returns:
            The reduced value
        """
        if not self.items:
            return initial
        
        if initial is None:
            result = self.items[0]
            start = 1
        else:
            result = initial
            start = 0
        
        for i in range(start, len(self.items)):
            result = callback(result, self.items[i])
        
        return result
    
    def sum(self):
        """
        Get the sum of all numeric items in the collection.
        
        Returns:
            The sum of all items
        """
        return sum(item for item in self.items if isinstance(item, (int, float)))
    
    def average(self):
        """
        Get the average of all numeric items in the collection.
        
        Returns:
            The average of all items
        """
        numeric_items = [item for item in self.items if isinstance(item, (int, float))]
        return sum(numeric_items) / len(numeric_items) if numeric_items else 0
    
    def max(self):
        """
        Get the maximum value in the collection.
        
        Returns:
            The maximum value
        """
        return max(self.items) if self.items else None
    
    def min(self):
        """
        Get the minimum value in the collection.
        
        Returns:
            The minimum value
        """
        return min(self.items) if self.items else None
    
    def sort(self, reverse=False):
        """
        Sort the collection.
        
        Args:
            reverse (bool): Whether to sort in descending order
            
        Returns:
            Collection: New sorted collection
        """
        sorted_items = sorted(self.items, reverse=reverse)
        return Collection(sorted_items)
    
    def unique(self):
        """
        Get unique items from the collection.
        
        Returns:
            Collection: New collection with unique items
        """
        seen = set()
        unique_items = []
        for item in self.items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)
        
        return Collection(unique_items)
    
    def chunk(self, size):
        """
        Chunk the collection into smaller collections of a given size.
        
        Args:
            size (int): Size of each chunk
            
        Returns:
            Collection: Collection of collections
        """
        chunks = []
        for i in range(0, len(self.items), size):
            chunk = self.items[i:i + size]
            chunks.append(Collection(chunk))
        
        return Collection(chunks)
    
    def where(self, key, operator=None, value=None):
        """
        Filter collection by a given key/value pair.
        
        Args:
            key: The key to filter by
            operator (str): Comparison operator ('=', '>', '<', etc.)
            value: The value to compare against
            
        Returns:
            Collection: Filtered collection
        """
        if operator is None and value is None:
            # Simple equality check
            filtered = [item for item in self.items if getattr(item, key, None) == value]
        else:
            # Operator-based filtering (basic implementation)
            # Note: For production use, consider implementing full operator support
            # Currently supports basic equality matching
            filtered = [item for item in self.items if getattr(item, key, None) == value]
        
        return Collection(filtered)
    
    def pluck(self, key):
        """
        Extract values for a given key from collection items.
        
        Args:
            key: The key to extract
            
        Returns:
            Collection: Collection of extracted values
        """
        values = []
        for item in self.items:
            if hasattr(item, key):
                values.append(getattr(item, key))
            elif isinstance(item, dict) and key in item:
                values.append(item[key])
        
        return Collection(values)
    
    def contains(self, item):
        """
        Check if the collection contains a given item.
        
        Args:
            item: Item to search for
            
        Returns:
            bool: True if item is found
        """
        return item in self.items
    
    def is_empty(self):
        """
        Check if the collection is empty.
        
        Returns:
            bool: True if collection is empty
        """
        return len(self.items) == 0
    
    def to_json(self):
        """
        Convert the collection to JSON string.
        
        Returns:
            str: JSON representation
        """
        import json
        return json.dumps(self.items)
    
    def __str__(self):
        """String representation of the collection."""
        return f"Collection({self.items})"
    
    def __repr__(self):
        """Representation of the collection."""
        return self.__str__()
    
    def __len__(self):
        """Length of the collection."""
        return len(self.items)
    
    def __iter__(self):
        """Make collection iterable."""
        return iter(self.items)
    
    def __getitem__(self, index):
        """Access items by index."""
        return self.items[index]


# Helper function for creating collections in Ludwig
def collect(items):
    """
    Create a new collection instance.
    
    Args:
        items: Items to create collection from
        
    Returns:
        Collection: New collection instance
    """
    return Collection(items)


# Example usage and tests
if __name__ == "__main__":
    # Test the collection functionality
    numbers = collect([1, 2, 3, 4, 5])
    
    print("Original:", numbers)
    print("Doubled:", numbers.map(lambda x: x * 2))
    print("Filtered (>2):", numbers.filter(lambda x: x > 2))
    print("Sum:", numbers.sum())
    print("Average:", numbers.average())
    print("Max:", numbers.max())
    print("Min:", numbers.min())
    
    # Test chaining
    result = collect([1, 2, 3, 4, 5]).map(lambda x: x * 2).filter(lambda x: x > 4)
    print("Chained operations:", result)
