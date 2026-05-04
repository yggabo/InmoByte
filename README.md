# InmoByte API

> A Flask REST API for real estate management systems

[![Python Version](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-lightgrey.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Team - Full Stack Web Development Course

| Role | Name | GitHub Profile |
|------|------|----------------|
| Product Owner | Gino Maranha | [![GitHub](https://img.shields.io/badge/@JuniorGino-181717?logo=github)](https://github.com/JuniorGino) |
| Scrum Master | Gabriel Hernandez | [![GitHub](https://img.shields.io/badge/@yggabo-181717?logo=github)](https://github.com/yggabo) |
| Developer | Jorge Cereceda | [![GitHub](https://img.shields.io/badge/@jorgecereceda-181717?logo=github)](https://github.com/jorgecereceda) |
| Developer | Yoandres La Cruz | [![GitHub](https://img.shields.io/badge/@ylcruzdev-181717?logo=github)](https://github.com/ylcruzdev) |

---

## About The Project

InmoByte is a comprehensive real estate management API built with Flask. The system allows property sellers to register their properties with real estate agents, who then manage interested clients, schedule property visits, and track transactions until closure (sale or rental).

### Key Features

- **User Authentication** - JWT-based auth with access/refresh tokens
- **Property Management** - Register, update, and track properties
- **Client Management** - Manage client information and preferences
- **Agent Assignment** - Assign agents to properties
- **Offer Management** - Track offers with status workflow
- **Appointment Scheduling** - Schedule and manage property visits
- **Advanced Filtering** - Filter properties by type, location, price, rooms, etc.
- **Role-Based Access** - Admin and Agent roles with different permissions

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Frontend)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST
┌───────────────────────────▼─────────────────────────────────┐
│                  Flask REST API (InmoByte)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Auth API   │  │  Properties  │  │   Offers     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Appointments │  │   Clients    │  │  Preferences │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────────┬─────────────────────────────────┘
                            │ SQLAlchemy ORM
┌───────────────────────────▼─────────────────────────────────┐
│                  MariaDB 11 Database                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Technologies Used

### Backend
- **Python 3.14** - Programming language
- **Flask 3.1.3** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM integration
- **SQLAlchemy 2.0** - Database ORM
- **Flask-JWT-Extended 4.7.1** - JWT authentication
- **Flask-Bcrypt 1.0.1** - Password hashing
- **Flask-Migrate 4.1.0** - Database migrations
- **Marshmallow 3.21.1** - Request/response validation

### Database
- **MariaDB 11** - Relational database
- **PyMySQL 1.1.2** - MySQL driver

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Gunicorn 25.3.0** - WSGI HTTP server
- **Adminer** - Database management UI (port 8080)

### Documentation & Testing
- **Flasgger 0.9.7.2** - Swagger/OpenAPI docs
- **pytest 9.0.2** - Testing framework
- **python-dotenv 1.2.2** - Environment variables

---

## Project Structure

```
InmoByte/
├── app/
│   ├── __init__.py              # Application factory
│   ├── core/                    # Core modules
│   │   ├── config.py            # Configuration classes
│   │   ├── extensions.py        # SQLAlchemy, JWT, Bcrypt
│   │   ├── cors_config.py       # CORS configuration
│   │   └── jwt_config.py        # JWT settings
│   └── api/                     # API blueprints
│       ├── auth/                # Authentication
│       ├── clients/             # Client management
│       ├── agents/              # Agent management
│       ├── register_and_assign_ownership/  # Properties
│       ├── offers/              # Offer management
│       ├── appointments_scheduling/  # Appointments
│       ├── preferences/         # Client preferences
│       └── filters_properties/  # Property filtering
├── tests/                       # Test suite (195+ tests)
├── scripts/                     # Utility scripts
├── migrations/                  # Database migrations
├── docker-compose.dev.yaml     # Docker configuration
├── requirements.txt             # Python dependencies
└── .env.example                # Environment variables template
```

---

## Database Models

### Entity Relationship Overview

**Core Models:**
- **Users** - Authentication credentials (username, email, password_hash)
- **UserProfile** - User details (name, phone, role)
- **Roles** - User roles (admin, agent)
- **Clients** - Property sellers/clients
- **Agents** - Real estate agents
- **Property** - Real estate properties
- **PropertyStatus** - Status (en venta, vendido, etc.)
- **Offer** - Purchase offers
- **OfferStatus** - Offer status (pendiente, aceptada, etc.)
- **Appointment** - Property visits
- **AppointmentStatus** - Appointment status
- **Preference** - Client property preferences

### Key Relationships:
- UserProfile ↔ Roles (many-to-one)
- UserProfile ↔ Users (one-to-one)
- Agents ↔ UserProfile (one-to-one)
- Properties ↔ Clients (many-to-one)
- Properties ↔ Agents (many-to-one)
- Offers ↔ Properties, Clients, OfferStatus
- Appointments ↔ Properties, Clients, Agents, AppointmentStatus
- Preferences ↔ Clients (one-to-one)

*See the `/docs` endpoint for full Swagger documentation with all fields.*

---

## API Endpoints

### Authentication (`/api/auth`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login and get JWT tokens | No |
| POST | `/api/auth/logout` | Logout (revoke token) | Yes |
| POST | `/api/auth/keep-alive` | Refresh token if expiring soon | Yes |

### Properties (`/api/register-and-assign-ownership/properties`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|-------------|---------------|
| GET | `/api/register-and-assign-ownership/properties` | List properties | Yes |
| POST | `/api/register-and-assign-ownership/properties` | Create property | Yes |
| GET | `/api/register-and-assign-ownership/properties/<id>` | Get property by ID | Yes |
| PUT | `/api/register-and-assign-ownership/properties/<id>` | Update property | Yes |
| DELETE | `/api/register-and-assign-ownership/properties/<id>` | Delete property | Yes |
| PATCH | `/api/register-and-assign-ownership/properties/<id>/assign-agent` | Assign agent | Yes |

### Offers (`/api/offers`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|-------------|---------------|
| GET | `/api/offers` | List offers | Yes |
| POST | `/api/offers/` | Create offer | Yes |
| GET | `/api/offers/<id>` | Get offer by ID | Yes |
| PATCH | `/api/offers/<id>/status` | Update offer status | Yes |

### Appointments (`/api/appointments`)
| Method | Endpoint | Description | Auth Required |
|--------|-----------|-------------|---------------|
| GET | `/api/appointments` | List appointments | Yes |
| POST | `/api/appointments` | Create appointment | Yes |
| PUT/PATCH | `/api/appointments/<id>` | Update appointment | Yes |
| DELETE | `/api/appointments/<id>` | Cancel appointment | Yes |

### Additional Endpoints
- **Clients** (`/api/clients`) - Full CRUD for client management
- **Agents** (`/api/agents`) - Full CRUD for agent management
- **User Profiles** (`/api/user-profile`) - User profile management
- **Roles** (`/api/roles`) - Role management
- **Property Status** (`/api/property-status`) - Property status management
- **Offer Status** (`/api/status-offers`) - Offer status management
- **Preferences** (`/api/preferences`) - Client preferences management
- **Filter Properties** (`/api/filter-properties`) - Advanced property filtering

**Full API documentation available at:** `http://localhost:7070/docs/` (when running)

---

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/InmoByte.git
cd InmoByte
```

2. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services
```bash
docker compose -f docker-compose.dev.yaml up --force-recreate --build
```

4. Access the application
- API: `http://localhost:7070`
- Swagger Docs: `http://localhost:7070/docs/`
- Adminer (DB): `http://localhost:8080`

### Run Tests
```bash
./scripts/run_tests.sh
```

### Seed Demo Data
```bash
./scripts/seed_demo.sh
```

---

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Flask
FLASK_APP=run.py
FLASK_ENV=development
FLASK_RUN_PORT=7070
SECRET_KEY=your-super-secret-key-with-32-chars-minimum
JWT_SECRET_KEY=your-jwt-secret-key-with-32-chars-minimum

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Database
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=app_db
DB_USER=mariadb
DB_PASSWORD=mariadb
DB_TEST_NAME=app_db_test
```

---

## Testing

The project includes comprehensive test coverage (195+ tests) using pytest.

### Run all tests
```bash
./scripts/run_tests.sh
```

### Run specific test file
```bash
./scripts/run_tests.sh -- tests/test_auth.py -v
```

### Test Coverage
- ✅ Authentication (register, login, logout)
- ✅ User Profiles and Roles
- ✅ Client Management
- ✅ Agent Management
- ✅ Property Management
- ✅ Offer Management
- ✅ Appointment Scheduling
- ✅ Property Filtering
- ✅ Preferences
- ✅ CORS Configuration
- ✅ JWT Handling

**Current Status:** 195 tests passing ✅

---

## API Documentation (Swagger)

Interactive API documentation is available via Swagger UI (Flasgger).

1. Start the application
2. Visit: `http://localhost:7070/docs/`
3. Explore and test all endpoints interactively

Each blueprint includes YAML documentation files in the `/docs` folder.

---

## Database Migrations

The project uses Flask-Migrate (Alembic) for database migrations.

### Create a migration
```bash
docker compose -f docker-compose.dev.yaml exec backend flask db migrate -m "Migration description"
```

### Apply migrations
```bash
docker compose -f docker-compose.dev.yaml exec backend flask db upgrade
```

---

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Workflow
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgments

- Full Stack Web Development Course
- Flask documentation and community
- SQLAlchemy documentation
- All open-source libraries used in this project

---

## Project Status

🚧 **In Development** - Core features implemented, tests passing ✅

- [x] Authentication system
- [x] Property management
- [x] Client management
- [x] Agent management
- [x] Offer management
- [x] Appointment scheduling
- [x] Property filtering
- [x] Comprehensive test suite (195 tests)
- [ ] Frontend integration
- [ ] Production deployment
