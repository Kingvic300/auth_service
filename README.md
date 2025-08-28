# Bill Station Auth Service

A robust Django authentication service with PostgreSQL, Redis caching, JWT authentication, and password reset functionality. Built for the Bill Station fintech platform.

## Features

- ✅ User registration with email as username
- ✅ JWT-based authentication
- ✅ Password reset with Redis-cached tokens
- ✅ Rate limiting on sensitive endpoints
- ✅ PostgreSQL database integration
- ✅ Redis caching for reset tokens
- ✅ Comprehensive API documentation with Swagger
- ✅ Docker support for local development
- ✅ Production-ready deployment configuration
- ✅ Comprehensive test suite

## Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT (Simple JWT)
- **Documentation**: Swagger/OpenAPI
- **Deployment**: Railway, Render
- **Containerization**: Docker

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | User registration | No |
| POST | `/api/auth/login/` | User login | No |
| POST | `/api/auth/logout/` | User logout | Yes |
| GET/PUT | `/api/auth/profile/` | User profile | Yes |
| POST | `/api/auth/forgot-password/` | Request password reset | No |
| POST | `/api/auth/reset-password/` | Reset password with token | No |

### Documentation Endpoints

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **JSON Schema**: `/swagger.json`

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- Docker (optional)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd auth_service
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database Setup**
```bash
# Create PostgreSQL database
createdb auth_service

# Run migrations
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Run Development Server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### Docker Development Setup

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Run migrations (in another terminal)**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Environment Variables

### Required Variables

```env
SECRET_KEY=your-secret-key-here
DEBUG=True/False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database
DB_NAME=auth_service
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Or use DATABASE_URL for production
DATABASE_URL=postgresql://user:password@host:port/database

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (optional for development)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@billstation.com
```

## API Usage Examples

### User Registration

```bash
curl -X POST http://localhost:8000/api/auth/register/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### User Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Access Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Password Reset Request

```bash
curl -X POST http://localhost:8000/api/auth/forgot-password/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com"
  }'
```

### Password Reset

```bash
curl -X POST http://localhost:8000/api/auth/reset-password/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "token": "reset-token-from-email",
    "new_password": "newsecurepassword123",
    "confirm_password": "newsecurepassword123"
  }'
```

## Deployment

### Railway Deployment

1. **Create Railway project**
```bash
railway login
railway init
```

2. **Add environment variables in Railway dashboard**
- `SECRET_KEY`: Generate a new secret key
- `DEBUG`: False
- `ALLOWED_HOSTS`: *.railway.app
- Add PostgreSQL and Redis services

3. **Deploy**
```bash
railway up
```

### Render Deployment

1. **Connect your GitHub repository to Render**
2. **Use the provided `render.yaml` configuration**
3. **Add environment variables in Render dashboard**
4. **Deploy automatically on git push**

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Rate Limiting

The following endpoints have rate limiting:

- **Login**: 5 requests per minute per IP
- **Forgot Password**: 3 requests per minute per IP  
- **Reset Password**: 3 requests per minute per IP

## Security Features

- Password validation with Django's built-in validators
- JWT token authentication with refresh tokens
- Rate limiting on sensitive endpoints
- CORS protection
- SQL injection protection via Django ORM
- XSS protection headers
- Password reset tokens with expiry (10 minutes)
- Secure password hashing with Django's PBKDF2

## Project Structure

```
auth_service/
├── auth_service/          # Django project configuration
│   ├── __init__.py
│   ├── settings.py        # Main settings
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── accounts/             # Authentication app
│   ├── __init__.py
│   ├── models.py         # User model
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   ├── urls.py           # App URLs
│   ├── utils.py          # Utility functions
│   └── tests.py          # Test cases
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose for development
├── railway.json         # Railway deployment config
├── render.yaml          # Render deployment config
├── .env.example         # Environment variables example
├── manage.py           # Django management script
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@billstation.com or create an issue in the repository.

## Deployment Links

- **Production API**: [Your Railway/Render URL]
- **API Documentation**: [Your Railway/Render URL]/swagger/
- **Admin Panel**: [Your Railway/Render URL]/admin/

---

Built with ❤️ by the Bill Station Team