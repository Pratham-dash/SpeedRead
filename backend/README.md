# SpeedRead Backend API

Flask-based REST API for speed reading text processing with Optimal Recognition Point (ORP) calculation.

## Architecture

```
backend/
├── app.py
├── config.py
├── requirements.txt          # Runtime deps (production/Render)
├── requirements-dev.txt      # Dev/test/lint deps
├── api/
├── services/
├── utils/
└── tests/
```

## Local setup

1. Create and activate a virtual environment.
2. Install dev dependencies:

```bash
cd /tmp/workspace/Pratham-dash/SpeedRead/backend
python3 -m pip install -r requirements-dev.txt
```

3. Create env file:

```bash
cp .env.example .env
```

4. Run backend:

```bash
python app.py
```

Backend runs on `http://localhost:5000` by default.

## Environment variables

Required for production:

- `FLASK_ENV=production`
- `DEBUG=False`
- `SECRET_KEY=<secure random value>`
- `CORS_ORIGINS=<comma-separated allowed frontend origins>`

Example:

```bash
CORS_ORIGINS=https://your-frontend.vercel.app,https://www.yourdomain.com
```

Notes:
- In development, if `CORS_ORIGINS` is unset, localhost origins are allowed by default.
- In production, `CORS_ORIGINS` must be explicitly set.

## API endpoints

- `GET /health`
- `GET /`
- `POST /api/process-text`
- `POST /api/calculate-orp`
- `GET /api/test`

## Testing and linting

```bash
cd /tmp/workspace/Pratham-dash/SpeedRead/backend
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
pytest tests/ -q
```

## Render deployment

Repository includes `/tmp/workspace/Pratham-dash/SpeedRead/render.yaml`.

Deploy flow:
1. Create a Render Blueprint service from the repository.
2. Confirm service uses:
   - `rootDir: backend`
   - `buildCommand: pip install -r requirements.txt`
   - `startCommand: gunicorn --bind 0.0.0.0:$PORT "app:create_app()"`
3. Set env vars in Render dashboard:
   - `FLASK_ENV=production`
   - `DEBUG=False`
   - `SECRET_KEY` (generated/secure)
   - `CORS_ORIGINS` (Vercel production + preview domains)
4. Validate:
   - `GET /health`
   - `GET /api/test`
