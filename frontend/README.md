# SpeedRead Frontend

Static vanilla JavaScript frontend for SpeedRead.

## Structure

```
frontend/
├── index.html
├── styles.css
├── config.js
└── app.js
```

## Local run

```bash
cd /tmp/workspace/Pratham-dash/SpeedRead/frontend
python3 -m http.server 8000
```

Open `http://localhost:8000`.

By default in local mode, `config.js` falls back to:

- `window.API_BASE_URL = http://localhost:5000/api`

## API base URL configuration

`frontend/config.js` supports runtime config via:

```js
window.__SPEEDREAD_CONFIG__ = {
  API_BASE_URL: "https://your-render-service.onrender.com/api"
};
```

If no runtime override is provided:
- localhost: falls back to `http://localhost:5000/api`
- non-localhost: falls back to `/api` (for proxy-based deployments)

## Vercel deployment

Repository includes `/tmp/workspace/Pratham-dash/SpeedRead/vercel.json` with static output from `frontend`.

Deploy flow:
1. Import repository into Vercel.
2. Ensure output directory is `frontend`.
3. Choose one backend-routing strategy:
   - Direct API URL: inject `window.__SPEEDREAD_CONFIG__.API_BASE_URL` to Render URL.
   - Proxy mode: configure Vercel rewrites so `/api/*` and `/health` route to Render backend.
4. Confirm frontend can:
   - Load page
   - Call backend health check
   - Process text via `/api/process-text`
