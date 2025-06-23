# Ludwig Complete Feature Guide

## 🚀 Quick Start

The fastest way to get started with Ludwig:

```bash
# One-command setup (interactive)
python ludwig_setup.py

# Or specify project details
python ludwig_setup.py my_blog web
```

This creates a complete web application with database, authentication, API, and modern UI components.

## 🎯 Core Features

### 1. **Modern Web Framework**
```ludwig
# Create web application
let app = create web_app do
    let name = "My App"
    let port = 3000
    let database = db_config
    let auth = auth_config

# Define routes
let routes = create routes do
    let home = route("GET", "/", "HomeController.index")
    let api_users = api_route("GET", "/api/users", "UserController.index")
```

### 2. **Database & ORM (Laravel-style)**
```ludwig
# Define models
let User = create model do
    let table_name = "users"
    let fillable = ["name", "email", "password"]
    let hidden = ["password"]

# Query database
let users = User.query()
    .where("active", true)
    .order_by("created_at", "desc")
    .paginate(1, 10)

# Create records
let user = User.create({
    "name": "John Doe",
    "email": "john@example.com",
    "password": hash_password("secret")
})
```

### 3. **Authentication System**
```ludwig
# Register user
let auth_result = AuthController.register({
    "name": "Jane Smith",
    "email": "jane@example.com", 
    "password": "password123"
})

# Login user
let login_result = AuthController.login({
    "email": "jane@example.com",
    "password": "password123"
})

# Returns JWT token for API access
```

### 4. **RESTful API Generation**
```bash
# Generate complete API resource
python artisan.py make:api posts --model

# Creates:
# - PostsController with CRUD operations
# - Post model with database mapping
# - Migration file for posts table
# - Routes: GET/POST/PUT/DELETE /api/posts
```

### 5. **UI Components (TailwindCSS + shadcn/ui)**
```ludwig
# Generate components
let hero = UIComponent.hero({
    "title": "Welcome to Ludwig",
    "subtitle": "Modern web development made simple",
    "cta_text": "Get Started",
    "cta_link": "/dashboard"
})

let data_table = UIComponent.table({
    "headers": ["Name", "Email", "Actions"],
    "rows": users.map(lambda user: [
        user.name, user.email,
        UIComponent.button({"text": "Edit", "variant": "outline"})
    ])
})
```

### 6. **Input Validation**
```ludwig
let validation_rules = {
    "name": ["required", "string", "min:2"],
    "email": ["required", "email", "unique:users"],
    "password": ["required", "string", "min:8"]
}

let validation = validate(user_data, validation_rules)
if validation.is_valid() do
    # Process data
else do
    # Handle errors: validation.errors()
```

### 7. **Collections (Laravel-style)**
```ludwig
let numbers = Collection.create([1, 2, 3, 4, 5])

let result = numbers
    .filter(lambda x: x > 2)
    .map(lambda x: x * 2)
    .sum()  # Returns 24

let users_collection = Collection.create(users)
    .group_by("department")
    .sort_by("name")
```

## 🛠️ Artisan CLI Commands

### Project Management
```bash
# Create new project
python artisan.py new my_blog web
python artisan.py new my_api web  
python artisan.py new my_cli cli

# Quick setup with all features
python ludwig_setup.py my_project web
```

### Code Generation
```bash
# Generate API resources
python artisan.py make:api users --model     # Full API with model
python artisan.py make:api posts --model     # Blog posts API

# Generate controllers
python artisan.py make:controller UserController
python artisan.py make:controller AuthController

# Generate UI components
python artisan.py make:component Header
python artisan.py make:component UserCard
python artisan.py make:component BlogPost

# Generate pages
python artisan.py make:page Dashboard
python artisan.py make:page Profile

# Generate middleware
python artisan.py make:middleware AuthMiddleware
python artisan.py make:middleware CorsMiddleware
```

### Database Operations
```bash
# Run migrations
python artisan.py migrate

# List migrations
ls migrations/

# Example migration files:
# migrations/2025_06_18_120000_create_users_table.ludwig
# migrations/2025_06_18_120001_create_posts_table.ludwig
```

### Development
```bash
# Start development server
python artisan.py dev

# Start Ludwig REPL
python artisan.py serve

# Run Ludwig file
python artisan.py run main.ludwig

# Build for production
python artisan.py build
```

### Information
```bash
# List available templates
python artisan.py templates

# List available components
python artisan.py components

# Show version
python artisan.py version

# Show help
python artisan.py help
```

## 📁 Project Structure

### Web Project Structure
```
my_blog/
├── app.ludwig              # Main application file
├── ludwig.json            # Project configuration
├── README.md              # Project documentation
├── controllers/           # Web controllers
│   ├── homecontroller.ludwig
│   ├── authcontroller.ludwig
│   └── userscontroller.ludwig
├── models/               # Database models
│   ├── user.ludwig
│   └── post.ludwig
├── migrations/           # Database migrations
│   ├── 2025_06_18_120000_create_users_table.ludwig
│   └── 2025_06_18_120001_create_posts_table.ludwig
├── components/           # UI components
│   ├── ui_components.ludwig
│   ├── header.ludwig
│   └── usercard.ludwig
├── views/               # HTML templates
│   ├── layout.html
│   ├── home.html
│   └── auth/
│       ├── login.html
│       └── register.html
├── public/              # Static assets
│   └── styles.css
├── lib/                 # Helper functions
│   └── helpers.ludwig
└── tests/               # Test files
    └── test_main.ludwig
```

## 🌐 API Endpoints

When you generate APIs with `make:api`, Ludwig automatically creates these endpoints:

### User API (`make:api users --model`)
```
GET    /api/users           # List all users (with pagination)
POST   /api/users           # Create new user
GET    /api/users/{id}      # Get specific user
PUT    /api/users/{id}      # Update user
DELETE /api/users/{id}      # Delete user
```

### Authentication API
```
POST   /api/auth/register   # Register new user
POST   /api/auth/login      # Login user
POST   /api/auth/logout     # Logout user (requires auth)
```

### Example API Responses
```json
// POST /api/auth/login
{
    "success": true,
    "message": "Login successful",
    "data": {
        "user": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        },
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "expires_in": 86400
    }
}

// GET /api/users
{
    "success": true,
    "message": "Success",
    "data": {
        "data": [...users...],
        "pagination": {
            "page": 1,
            "limit": 10,
            "total": 50,
            "pages": 5
        }
    }
}
```

## 🎨 UI Components

Ludwig includes pre-built components compatible with TailwindCSS and shadcn/ui:

### Available Components
- `button` - Various button styles and sizes
- `card` - Content cards with headers and actions
- `input` - Form inputs with validation
- `form` - Complete forms with validation
- `table` - Data tables with sorting and pagination
- `navigation` - Navigation bars and menus
- `modal` - Modal dialogs and popups
- `alert` - Success, error, and info alerts
- `avatar` - User avatars and profile pictures
- `hero` - Hero sections for landing pages
- `features_grid` - Feature showcase grids
- `stats_card` - Statistics and metrics cards
- `auth_form` - Login and registration forms

### Using Components
```ludwig
# Generate component file
python artisan.py make:component ProductCard

# Use in controllers
let product_card = UIComponent.card({
    "title": product.name,
    "content": product.description,
    "image": product.image_url,
    "actions": [
        UIComponent.button({"text": "Buy Now", "variant": "primary"}),
        UIComponent.button({"text": "Details", "variant": "outline"})
    ]
})
```

## 🔐 Authentication & Security

### Password Security
- PBKDF2 hashing with 100,000 iterations
- Random salt generation
- Constant-time comparison to prevent timing attacks

### JWT Tokens
- HS256 signature algorithm
- Configurable expiration time
- Automatic token validation middleware

### Middleware
```ludwig
# Authentication middleware
let auth_middleware = create middleware do
    let token = get_request_header("Authorization")
    let user = verify_jwt_token(token)
    if not user do
        return redirect("/login")

# Apply to routes
let protected_route = route("GET", "/dashboard", "DashboardController.index", ["auth"])
```

## 📊 Database Features

### Migrations
```ludwig
# Create migration
python artisan.py make:migration create_posts_table

# Migration file example
let CreatePostsTable = create migration do
    let up = create action do
        create_table("posts") do |table|
            table.id()
            table.string("title").not_null()
            table.text("content").nullable()
            table.foreign_key("user_id").references("users.id")
            table.timestamps()
    
    let down = create action do
        drop_table("posts")
```

### Relationships
```ludwig
# One-to-Many
let user_posts = create relationship do
    return has_many("Post", "user_id")

# Belongs-To
let post_user = create relationship do
    return belongs_to("User", "user_id")

# Many-to-Many
let post_tags = create relationship do
    return belongs_to_many("Tag", "post_tags", "post_id", "tag_id")
```

### Query Builder
```ludwig
let posts = Post.query()
    .where("published", true)
    .where("created_at", ">", "2025-01-01")
    .order_by("title")
    .with("user", "tags")
    .paginate(1, 10)
```

## 🚀 Deployment & Production

### Build for Production
```bash
python artisan.py build
```

### Configuration
```ludwig
# config/app.ludwig
let production_config = {
    "debug": false,
    "database": {
        "driver": "postgresql",
        "host": "your-db-host",
        "database": "your-db-name"
    },
    "auth": {
        "jwt_secret": "your-secure-secret-key"
    }
}
```

## 🔧 Advanced Features

### Custom Validation Rules
```ludwig
# Create custom validator
let custom_validator = create validator do
    let validate_username = create rule do
        # Custom validation logic
        return value.length >= 3 and value.match(/^[a-zA-Z0-9_]+$/)
```

### Custom Middleware
```ludwig
# Rate limiting middleware
let rate_limit_middleware = create middleware do
    let client_ip = get_client_ip()
    let request_count = get_cache("rate_limit:" + client_ip)
    
    if request_count > 100 do
        return json_error("Rate limit exceeded", {}, 429)
```

### Background Jobs
```ludwig
# Queue jobs for background processing
let email_job = create job do
    let send_welcome_email = create action do
        # Send email logic
        send_email(user.email, "Welcome to " + app_name)

# Dispatch job
dispatch_job(email_job, {"user_id": user.id})
```

## 📖 Examples

### Complete Blog Application
```bash
# Create blog project
python ludwig_setup.py my_blog web

cd my_blog

# Generate blog resources
python ../artisan.py make:api posts --model
python ../artisan.py make:api comments --model
python ../artisan.py make:api categories --model

# Generate UI components
python ../artisan.py make:component PostCard
python ../artisan.py make:component CommentList
python ../artisan.py make:component CategoryFilter

# Start development
python ../artisan.py dev
```

### E-commerce API
```bash
# Create e-commerce project
python ludwig_setup.py my_shop web

cd my_shop

# Generate commerce resources
python ../artisan.py make:api products --model
python ../artisan.py make:api orders --model
python ../artisan.py make:api customers --model
python ../artisan.py make:api payments --model

# Start development
python ../artisan.py dev
```

## 🎓 Learning Resources

1. **Start with Quick Setup**: Use `python ludwig_setup.py` for immediate hands-on experience
2. **Explore Generated Code**: Look at the generated controllers, models, and components
3. **Read DEVELOPMENT_SUMMARY.md**: Comprehensive language features and syntax
4. **Experiment with APIs**: Test the generated endpoints with curl or Postman
5. **Customize Components**: Modify the UI components to match your design

## 🤝 Contributing

Ludwig is open source and welcomes contributions:

1. **Report Issues**: Found a bug? Create an issue
2. **Suggest Features**: Have ideas for improvements? Share them
3. **Submit Pull Requests**: Code contributions are welcome
4. **Improve Documentation**: Help make Ludwig more accessible

## 📞 Support

- **Documentation**: Check README.md and DEVELOPMENT_SUMMARY.md
- **Examples**: Look at generated projects for patterns
- **Community**: Join discussions and share your projects

Ludwig makes modern web development simple, elegant, and productive. Start building today! 🚀
