# Insurance Management Project

A Django-based insurance portal for managing policies, customers, claims, and reporting.

## 📁 Repository Structure

- `main_app/` - Django application modules and business logic
- `requirements.txt` - Python package dependencies
- `README.md` - Project guidance (this file)

### In `main_app/`
- `analytics.py` - analytics utilities
- `fraud_detection.py` - fraud detection logic
- `policy_recommendation.py` - recommendation engine
- `tests/` - unit tests for authentication and domain logic
- `management/commands/populate_data.py` - sample data loader command
- `migrations/` - DB schema migration history

## 🚀 Quick Start

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply Django migrations:
   ```bash
   python manage.py migrate
   ```
4. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
5. Run development server:
   ```bash
   python manage.py runserver
   ```

Then open `http://127.0.0.1:8000` to use the portal.

## 🧪 Testing

Run unit tests:
```bash
python manage.py test
```

## 🔧 Common Commands

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`
- `python manage.py test`

## 📦 Deployment Notes

1. Use environment variables for sensitive values (SECRET_KEY, DB credentials).
2. In production, use a real database (PostgreSQL/MySQL), not SQLite.
3. Use `gunicorn` and a reverse proxy (e.g. nginx) for production.

## 🤝 Contribution

1. Fork and branch (`feature/<name>`).
2. Add tests for new features.
3. Submit a PR with clear description.

## 📌 Project Goals

- Manage users and agent roles
- Create/update insurance policies
- Submit and process claims
- Provide analytics and recommendation insights

---

If you want, I can also add a `.gitignore` and Python project scaffolding so this repo is ready to run in one command.
