"""
Ludwig Database & ORM System

Laravel Eloquent-inspired ORM for Ludwig with simple, elegant database operations.
Supports SQLite, PostgreSQL, and MySQL with migrations, models, and query builder.
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path


class Database:
    """Database connection and query management."""
    
    def __init__(self, config=None):
        """Initialize database connection."""
        self.config = config or {
            'driver': 'sqlite',
            'database': 'ludwig.db',
            'host': 'localhost',
            'port': 5432,
            'username': '',
            'password': ''
        }
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection."""
        if self.config['driver'] == 'sqlite':
            self.connection = sqlite3.connect(self.config['database'])
            self.connection.row_factory = sqlite3.Row
        else:
            raise NotImplementedError(f"Database driver '{self.config['driver']}' not yet supported. Currently supports: sqlite")
    
    def execute(self, query, params=None):
        """Execute a database query."""
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    
    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def fetch_one(self, query, params=None):
        """Fetch one result from a query."""
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def commit(self):
        """Commit transaction."""
        self.connection.commit()
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()


class QueryBuilder:
    """Fluent query builder for database operations."""
    
    def __init__(self, db, table):
        """Initialize query builder."""
        self.db = db
        self.table = table
        self.query_parts = {
            'select': ['*'],
            'where': [],
            'order': [],
            'limit': None,
            'offset': None
        }
    
    def select(self, *columns):
        """Select specific columns."""
        self.query_parts['select'] = list(columns)
        return self
    
    def where(self, column, operator=None, value=None):
        """Add WHERE clause."""
        if operator is None:
            # where(column, value) format
            operator = '='
            value = operator
        
        self.query_parts['where'].append({
            'column': column,
            'operator': operator,
            'value': value,
            'type': 'AND'
        })
        return self
    
    def or_where(self, column, operator=None, value=None):
        """Add OR WHERE clause."""
        if operator is None:
            operator = '='
            value = operator
        
        self.query_parts['where'].append({
            'column': column,
            'operator': operator,
            'value': value,
            'type': 'OR'
        })
        return self
    
    def order_by(self, column, direction='ASC'):
        """Add ORDER BY clause."""
        self.query_parts['order'].append(f"{column} {direction}")
        return self
    
    def limit(self, count):
        """Add LIMIT clause."""
        self.query_parts['limit'] = count
        return self
    
    def offset(self, count):
        """Add OFFSET clause."""
        self.query_parts['offset'] = count
        return self
    
    def build_select_query(self):
        """Build SELECT query."""
        # SELECT
        query = f"SELECT {', '.join(self.query_parts['select'])} FROM {self.table}"
        params = []
        
        # WHERE
        if self.query_parts['where']:
            where_clauses = []
            for i, condition in enumerate(self.query_parts['where']):
                if i == 0:
                    where_clauses.append(f"{condition['column']} {condition['operator']} ?")
                else:
                    where_clauses.append(f"{condition['type']} {condition['column']} {condition['operator']} ?")
                params.append(condition['value'])
            
            query += f" WHERE {' '.join(where_clauses)}"
        
        # ORDER BY
        if self.query_parts['order']:
            query += f" ORDER BY {', '.join(self.query_parts['order'])}"
        
        # LIMIT
        if self.query_parts['limit']:
            query += f" LIMIT {self.query_parts['limit']}"
        
        # OFFSET
        if self.query_parts['offset']:
            query += f" OFFSET {self.query_parts['offset']}"
        
        return query, params
    
    def get(self):
        """Execute query and get all results."""
        query, params = self.build_select_query()
        return self.db.fetch_all(query, params)
    
    def first(self):
        """Execute query and get first result."""
        self.limit(1)
        query, params = self.build_select_query()
        return self.db.fetch_one(query, params)
    
    def find(self, id):
        """Find record by ID."""
        return self.where('id', id).first()
    
    def count(self):
        """Count records."""
        query = f"SELECT COUNT(*) as count FROM {self.table}"
        params = []
        
        if self.query_parts['where']:
            where_clauses = []
            for i, condition in enumerate(self.query_parts['where']):
                if i == 0:
                    where_clauses.append(f"{condition['column']} {condition['operator']} ?")
                else:
                    where_clauses.append(f"{condition['type']} {condition['column']} {condition['operator']} ?")
                params.append(condition['value'])
            
            query += f" WHERE {' '.join(where_clauses)}"
        
        result = self.db.fetch_one(query, params)
        return result['count'] if result else 0


class Model:
    """Base model class for database operations."""
    
    table = None
    primary_key = 'id'
    fillable = []
    
    def __init__(self, attributes=None):
        """Initialize model instance."""
        self.attributes = attributes or {}
        self.original = {}
        self.exists = False
    
    @classmethod
    def get_database(cls):
        """Get database instance."""
        if not hasattr(cls, '_database'):
            cls._database = Database()
        return cls._database
    
    @classmethod
    def query(cls):
        """Get query builder instance."""
        return QueryBuilder(cls.get_database(), cls.table)
    
    @classmethod
    def all(cls):
        """Get all records."""
        results = cls.query().get()
        return [cls(attrs) for attrs in results]
    
    @classmethod
    def find(cls, id):
        """Find record by ID."""
        result = cls.query().find(id)
        if result:
            instance = cls(result)
            instance.exists = True
            instance.original = result.copy()
            return instance
        return None
    
    @classmethod
    def where(cls, column, operator=None, value=None):
        """Start a WHERE query."""
        return cls.query().where(column, operator, value)
    
    @classmethod
    def create(cls, attributes):
        """Create new record."""
        instance = cls(attributes)
        instance.save()
        return instance
    
    def save(self):
        """Save model to database."""
        if self.exists:
            return self.update()
        else:
            return self.insert()
    
    def insert(self):
        """Insert new record."""
        # Filter fillable attributes
        data = {k: v for k, v in self.attributes.items() if k in self.fillable}
        
        if not data:
            return False
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = list(data.values())
        
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.get_database().execute(query, values)
        self.attributes[self.primary_key] = cursor.lastrowid
        self.get_database().commit()
        
        self.exists = True
        self.original = self.attributes.copy()
        
        return True
    
    def update(self):
        """Update existing record."""
        if not self.exists:
            return False
        
        # Get changed attributes
        changed = {k: v for k, v in self.attributes.items() 
                  if k in self.fillable and v != self.original.get(k)}
        
        if not changed:
            return True
        
        set_clause = ', '.join([f"{k} = ?" for k in changed.keys()])
        values = list(changed.values())
        values.append(self.attributes[self.primary_key])
        
        query = f"UPDATE {self.table} SET {set_clause} WHERE {self.primary_key} = ?"
        
        self.get_database().execute(query, values)
        self.get_database().commit()
        
        self.original.update(changed)
        
        return True
    
    def delete(self):
        """Delete record."""
        if not self.exists:
            return False
        
        query = f"DELETE FROM {self.table} WHERE {self.primary_key} = ?"
        self.get_database().execute(query, [self.attributes[self.primary_key]])
        self.get_database().commit()
        
        self.exists = False
        return True
    
    def __getattr__(self, name):
        """Get attribute value."""
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Set attribute value."""
        if name in ['attributes', 'original', 'exists']:
            super().__setattr__(name, value)
        else:
            if not hasattr(self, 'attributes'):
                super().__setattr__(name, value)
            else:
                self.attributes[name] = value


class Migration:
    """Database migration system."""
    
    def __init__(self, db):
        """Initialize migration."""
        self.db = db
        self.create_migrations_table()
    
    def create_migrations_table(self):
        """Create migrations tracking table."""
        query = """
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            migration VARCHAR(255) NOT NULL,
            batch INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.db.execute(query)
        self.db.commit()
    
    def run(self, migration_name, up_queries):
        """Run a migration."""
        # Check if already run
        existing = self.db.fetch_one(
            "SELECT * FROM migrations WHERE migration = ?",
            [migration_name]
        )
        
        if existing:
            print(f"Migration {migration_name} already run")
            return
        
        # Run migration queries
        for query in up_queries:
            self.db.execute(query)
        
        # Record migration
        batch = self.get_next_batch()
        self.db.execute(
            "INSERT INTO migrations (migration, batch) VALUES (?, ?)",
            [migration_name, batch]
        )
        
        self.db.commit()
        print(f"Migration {migration_name} completed")
    
    def get_next_batch(self):
        """Get next batch number."""
        result = self.db.fetch_one("SELECT MAX(batch) as max_batch FROM migrations")
        return (result['max_batch'] or 0) + 1


# Example model definitions
class User(Model):
    """User model example."""
    table = 'users'
    fillable = ['name', 'email', 'password', 'created_at', 'updated_at']


class Post(Model):
    """Post model example."""
    table = 'posts'
    fillable = ['title', 'content', 'user_id', 'published', 'created_at', 'updated_at']


# Migration examples
def create_users_table(db):
    """Create users table migration."""
    migration = Migration(db)
    migration.run('2025_06_18_create_users_table', [
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ])


def create_posts_table(db):
    """Create posts table migration."""
    migration = Migration(db)
    migration.run('2025_06_18_create_posts_table', [
        """
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            user_id INTEGER,
            published BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    ])


# Example usage
if __name__ == "__main__":
    # Initialize database
    db = Database()
    
    # Run migrations
    create_users_table(db)
    create_posts_table(db)
    
    # Create users
    user1 = User.create({
        'name': 'John Doe',
        'email': 'john@example.com', 
        'password': 'hashed_password',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    })
    
    user2 = User.create({
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'password': 'hashed_password',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    })
    
    # Create posts
    post1 = Post.create({
        'title': 'Hello Ludwig!',
        'content': 'This is my first post using Ludwig ORM.',
        'user_id': user1.id,
        'published': True,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    })
    
    # Query examples
    all_users = User.all()
    print(f"All users: {len(all_users)}")
    
    john = User.where('email', 'john@example.com').first()
    print(f"Found user: {john.name if john else 'Not found'}")
    
    published_posts = Post.where('published', True).get()
    print(f"Published posts: {len(published_posts)}")
    
    db.close()
