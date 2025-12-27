# TrueLine News - Deployment Guide

This guide explains how to take the TrueLine News app live for public access.

## 1) Quick Checklist
- Domain name registered (e.g., trueline.example)
- DNS control for the domain
- Cloud account (AWS, Azure, GCP, or any VPS)
- Docker + Docker Compose installed on the server
- TLS certificates (use Lets Encrypt via certbot)

## 2) Production Configuration
Create a `.env` file on the server (never commit secrets):
```
# Flask
FLASK_APP=app
FLASK_ENV=production
FLASK_DEBUG=0

# MongoDB
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_DB=trueline_news
MONGODB_USER=admin
MONGODB_PASSWORD=strong-password

# App
API_TIMEOUT=10
MAX_CONTENT_LENGTH=5242880
LOG_LEVEL=INFO
```

## 3) Build and Run (Server)
```bash
# 1) Pull code
git clone https://github.com/<your-org>/TrueLine-News.git
cd TrueLine-News

# 2) Start services
sudo docker-compose up -d

# 3) Verify
curl -f http://localhost/api/health
```

## 4) Expose to the Internet
1. Point your domain DNS `A` record to the server public IP.
2. Update frontend nginx config to use your domain:
```
server_name trueline.example;
```
3. Add HTTPS with Lets Encrypt (certbot):
```bash
sudo apt-get update && sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d trueline.example -d www.trueline.example
```
4. Reload nginx:
```bash
sudo docker-compose restart frontend
```

## 5) Environment Hardening
- Use strong MongoDB credentials; change default passwords.
- Open only required ports: 80/443 (frontend), 27017 closed to public.
- Set `FLASK_ENV=production` and `FLASK_DEBUG=0`.
- Add rate limiting on `/api/*` (nginx `limit_req` if needed).
- Configure log rotation (Docker handles basic rotation, but consider a log driver like `local` with size caps).

## 6) Data and Backups
- MongoDB volume: `mongodb_data` (persisted by docker-compose).
- Schedule backups using `mongodump` (cron or GitHub Actions with secure storage).
- Consider MongoDB Atlas if you prefer managed DB; then set `MONGODB_HOST` to the Atlas URI.

## 7) Scaling Options
- Vertical: increase server CPU/RAM.
- Horizontal: run multiple backend containers behind a load balancer; keep MongoDB single primary (or use managed).
- Add a CDN for static assets if needed.

## 8) Monitoring & Alerts
- Enable nginx access/error logs (already on).
- Add uptime monitoring (Pingdom/UptimeRobot).
- Consider Sentry for backend error tracking.
- Track container health: `docker ps`, `docker logs`, `docker stats`.

## 9) Common Commands
```bash
# Restart all
sudo docker-compose restart

# Rebuild after code changes
sudo docker-compose down
sudo docker-compose up -d --build

# Check logs
sudo docker-compose logs -f backend
sudo docker-compose logs -f frontend

# Check health
curl -f http://localhost/api/health
```

## 10) Post-Deployment Smoke Test
- Open https://trueline.example in browser.
- Confirm CSS/JS load (no console errors).
- Hit `https://trueline.example/api/health` returns healthy.
- Verify articles list and verification endpoint respond 200.

## 11) If CSS/JS Dont Load
- Hard refresh (Ctrl+Shift+R).
- Ensure nginx `include /etc/nginx/mime.types;` is present (already configured).
- Verify `docker-compose restart frontend` after any nginx change.

Youre live! 🚀
