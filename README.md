# Rental Project

Back-end REST API for a housing rental platform built with Django REST Framework.

## Tech Stack

- **Python 3.13** / **Django 6.0**
- **Django REST Framework** — API
- **JWT** (SimpleJWT) — authentication
- **SQLite** — database (local)
- **django-filter** — filtering

## Features

- User registration and authentication via JWT
- Two user roles: **tenant** and **landlord**
- Listings management (CRUD)
- Keyword search, filtering and sorting
- Booking system with confirm/reject flow
- Reviews and ratings
- Search history and view history analytics

## Setup & Installation

```bash
# Clone the repository
git clone <url>
cd rental_project

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env if needed

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Server will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Users
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/users/register/` | Register a new user |
| POST | `/api/users/login/` | Login and get JWT tokens |
| POST | `/api/users/logout/` | Logout (blacklist refresh token) |
| GET | `/api/users/profile/` | Get current user profile |
| POST | `/api/users/token/refresh/` | Refresh access token |

### Listings
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/listings/` | List all active listings (search, filter, sort) |
| POST | `/api/listings/create/` | Create a listing (landlord only) |
| GET | `/api/listings/my/` | Get my listings |
| GET | `/api/listings/<id>/` | Get listing details |
| PUT/PATCH | `/api/listings/<id>/update/` | Update listing (owner only) |
| DELETE | `/api/listings/<id>/delete/` | Delete listing (owner only) |
| PATCH | `/api/listings/<id>/toggle-status/` | Toggle active/inactive status |

### Search & Filtering

GET `/api/listings/` supports the following query parameters:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `search` | `?search=berlin` | Search in title and description |
| `price_min` | `?price_min=500` | Minimum price |
| `price_max` | `?price_max=2000` | Maximum price |
| `rooms_min` | `?rooms_min=2` | Minimum number of rooms |
| `rooms_max` | `?rooms_max=4` | Maximum number of rooms |
| `location` | `?location=Berlin` | Filter by city or district |
| `property_type` | `?property_type=apartment` | Filter by property type |
| `ordering` | `?ordering=price` | Sort by: `price`, `-price`, `created_at`, `-created_at`, `views_count` |

### Bookings
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/bookings/` | Create a booking (tenant only) |
| GET | `/api/bookings/my/` | Get my bookings |
| GET | `/api/bookings/incoming/` | Get incoming bookings (landlord) |
| PATCH | `/api/bookings/<id>/cancel/` | Cancel a booking |
| PATCH | `/api/bookings/<id>/confirm/` | Confirm a booking (landlord) |
| PATCH | `/api/bookings/<id>/reject/` | Reject a booking (landlord) |

### Reviews
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/listings/<id>/reviews/` | Get all reviews for a listing |
| POST | `/api/listings/<id>/reviews/create/` | Leave a review (tenant with confirmed booking only) |

### Analytics
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/analytics/search-history/` | My search history |
| GET | `/api/analytics/popular-searches/` | Popular search keywords |
| GET | `/api/analytics/view-history/` | My recently viewed listings |
| GET | `/api/analytics/popular-listings/` | Most viewed listings |

## Authentication

All protected endpoints require the following header:
```
Authorization: Bearer <access_token>
```

## Property Types

`apartment`, `house`, `studio`, `room`, `other`

## Admin Panel

`http://127.0.0.1:8000/admin/`
