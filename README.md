# HireMe

HireMe is a production-style Django 5 mini freelance marketplace (simplified Upwork). It ships with role-based dashboards, freelancer portfolios, hire requests, real-time chat, and real-time notifications.

## Highlights
- Custom user model with email login and roles (Freelancer, Client)
- Role-based dashboards with stats, activity, and alerts
- Freelancer profiles with skills, education, projects, and screenshots
- Public directory and SEO-friendly freelancer profiles
- Hire requests with status workflow and attachments
- Real-time messaging and notifications via Django Channels + WebSockets
- Bootstrap 5 CDN UI with responsive layouts
- Sitemap and robots.txt for SEO

## Tech Stack
- Django 5.x, Python 3.11+
- Django Channels + Redis (production)
- PostgreSQL (production), SQLite (development)
- Bootstrap 5 via CDN

## Project Structure
Apps included:
- `accounts` - custom user model, auth, dashboards
- `profiles` - freelancer profile, skills, education, projects
- `marketplace` - public browse and freelancer profiles
- `requests` - hire requests and status workflow
- `messaging` - chat threads and messages
- `notifications` - in-app notifications + WebSockets
- `core` - marketing pages, sitemap, robots

## Quick Start (Dev)
1. Create a virtual environment.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Copy environment file:
   - Windows:
     ```powershell
     copy .env.example .env
     ```
   - macOS/Linux:
     ```bash
     cp .env.example .env
     ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the server:
   ```bash
   python manage.py runserver
   ```
7. Open `http://127.0.0.1:8000/`.

## Real-Time (WebSockets)
WebSockets are served via ASGI. If you see `/ws/notifications/` 404s, make sure:
- `daphne` is installed (included in `requirements.txt`)
- You are running the dev server with `python manage.py runserver`

You can also run Daphne directly:
```bash
python -m daphne hireme.asgi:application
```

## Redis (Channels Layer)
Redis is required for real-time features in production. For local dev:
```bash
redis-server
```
Set `REDIS_URL` in `.env` (example: `redis://127.0.0.1:6379/0`).

## Environment Variables
The app reads from `.env` (see `.env.example`):
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`
- `REDIS_URL`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`

## Production Notes
Set:
- `DJANGO_SETTINGS_MODULE=hireme.settings.prod`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`
- `POSTGRES_*` variables
- `EMAIL_*` for SMTP
- `REDIS_URL` for Channels

Then run:
```bash
python manage.py migrate
python manage.py collectstatic
```

## Usage Walkthrough
1. Register as a Freelancer or Client.
2. Freelancers build profiles (skills, education, projects).
3. Clients browse `/freelancers/` and send hire requests.
4. Each request creates a thread for chat.
5. Notifications and unread counters update in real time.

## Tests
```bash
python manage.py test
```

## Contributing
Pull requests are welcome. Please:
- Create a feature branch
- Keep changes focused
- Add tests for new behavior when possible

## License
Add a LICENSE file to define how the project can be used.
