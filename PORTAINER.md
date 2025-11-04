# Portainer Deployment

## Quick Deploy

1. **In Portainer:** Go to Stacks → Add Stack

2. **Name:** `vape-juice-manager`

3. **Paste this stack:**

```yaml
version: '3.8'

services:
  vape-manager:
    image: ghcr.io/billsbdb3/vape-mixing-manager:latest
    container_name: vape-juice-manager
    ports:
      - "5001:5001"
    volumes:
      - vape-data:/app/vape_data.json
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - GOOGLE_API_KEY=your-google-api-key-here

volumes:
  vape-data:
```

**Important:** Replace `your-google-api-key-here` with your actual Google API key for AI features to work.

4. **Click "Deploy the stack"**

5. **Access:** `http://your-server-ip:5001`

## Update to Latest Version

In Portainer:
1. Go to your stack
2. Click "Pull and redeploy"

Or manually:
```bash
docker pull ghcr.io/billsbdb3/vape-mixing-manager:latest
docker-compose up -d
```

## Custom Port

To use a different port, change the first number:
```yaml
ports:
  - "8080:5001"  # Access on port 8080
```

## Environment Variables

To set a custom API key without rebuilding:
```yaml
environment:
  - FLASK_ENV=production
  - GOOGLE_API_KEY=your-api-key-here
```

Then update `vape_app.py` to use:
```python
GEMINI_API_KEY = os.environ.get('GOOGLE_API_KEY', 'default-key')
```
